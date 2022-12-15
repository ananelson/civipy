import json
import requests
import subprocess
from typing import Callable, Optional, Any

from civipy.config import SETTINGS
from civipy.config import logger
from civipy.exceptions import CiviProgrammingError
from civipy.exceptions import CiviAPIError
from civipy.exceptions import CiviHTTPError


def assert_unique(response):
    if not 'count' in response:
        raise CiviProgrammingError("no count in response!")
    assert response['count'] == 1, response


def get_unique(response):
    if isinstance(response['values'], dict):
        ident = list(response['values'].keys())[0]
        return get_unique_value_for_id(ident, response)
    else:
        return get_unique_value(response)


def get_unique_value(response):
    assert_unique(response)
    return response['values'][0]


def get_unique_value_for_id(contact_id, response):
    assert response['count'] == 1, response
    return response['values'][contact_id]


class CiviCRMBase(object):
    REPR_FIELDS = ["display_name", "name"]

    @classmethod
    def _entity(cls, entity=None):
        if entity is None:
            entity = cls.__name__[4:]
            if entity == "CRMBase":
                raise CiviProgrammingError("Must provide entity")
        return entity

    @classmethod
    def _params(cls, entity, action, kwargs):
        entity = cls._entity(entity)
        params = {
            'entity' : entity,
            'action' : action,
            'api_key' : SETTINGS.user_key,
            'debug' : 1,
            'key' : SETTINGS.site_key,
            'json' : 1,
            'sequential': 1,
        }
        params.update(kwargs)
        return params

    @classmethod
    def process_http_response(cls, r):
        logger.debug(r.url)
        if r.status_code == 200:
            return cls.process_json_response(r.json())
        else:
            raise CiviHTTPError(r)

    @classmethod
    def process_json_response(cls, data):
        if 'is_error' in data and data['is_error'] == 1:
            raise CiviAPIError(data)
        return data

    @classmethod
    def http_get(cls, action, entity, kwargs):
        params = cls._params(entity, action, kwargs)
        logger.debug(str(params))
        r = requests.get(
                SETTINGS.rest_base,
                params = params)
        return cls.process_http_response(r)

    @classmethod
    def http_post(cls, action, entity, kwargs):
        params = cls._params(entity, action, kwargs)
        logger.debug(str(params))
        r = requests.post(
                SETTINGS.rest_base,
                params = params)
        return cls.process_http_response(r)

    @classmethod
    def run_drush_process(cls, action, entity, params):
        entity = cls._entity(entity)
        # use Popen directly since many nice features of run() were not added until Python 3.7
        p = subprocess.Popen([SETTINGS.rest_base, "cvapi", "--out=json", "--in=json", "%s.%s" % (entity, action)],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(json.dumps(params).encode("UTF-8"))
        return cls.process_json_response(json.loads(stdout.decode("UTF-8")))

    @classmethod
    def run_cvcli_process(cls, action, entity, params):
        entity = cls._entity(entity)
        # use Popen directly since many nice features of run() were not added until Python 3.7
        # cli.php -e entity -a action [-u user] [-s site] [--output|--json] [PARAMS]
        params = ["--%s=%s" % (k, v) for k, v in params.items()]
        p = subprocess.Popen([SETTINGS.rest_base, "-e", entity, "-a", action, "--json"] + params,
                stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return cls.process_json_response(json.loads(stdout.decode("UTF-8")))

    @classmethod
    def _get_method(cls) -> Callable[[str, Optional[str], Any], Any]:
        if SETTINGS.api_type == 'http':
            return cls.http_get
        elif SETTINGS.api_type == 'drush':
            return cls.run_drush_process
        elif SETTINGS.api_type == 'cvcli':
            return cls.run_cvcli_process
        else:
            raise CiviProgrammingError("not implemented %s" % SETTINGS.api_type)

    @classmethod
    def _post_method(cls) -> Callable[[str, Optional[str], Any], Any]:
        if SETTINGS.api_type == 'http':
            return cls.http_post
        elif SETTINGS.api_type == 'drush':
            return cls.run_drush_process
        elif SETTINGS.api_type == 'cvcli':
            return cls.run_cvcli_process
        else:
            raise CiviProgrammingError("not implemented %s" % SETTINGS.api_type)

    @classmethod
    def _get(cls, entity=None, **kwargs):
        """
        Calls the CiviCRM API get action and returns parsed JSON on success.
        """
        return cls._get_method()('get', entity, kwargs)

    @classmethod
    def _getsingle(cls, entity, **kwargs):
        """
        Calls the CiviCRM API getsingle action and returns parsed JSON on success.
        """
        return cls._get_method()('getsingle', entity, kwargs)

    @classmethod
    def _create(cls, entity=None, **kwargs):
        """
        Calls the CiviCRM API create action and returns parsed JSON on success.
        """
        return cls._post_method()('create', entity, kwargs)

    @classmethod
    def _search_query(cls, search_key_name, kwargs):
        if search_key_name == 'id' and not search_key_name in kwargs:
            # search_key_name is not specified, assume all of kwargs corresponds to search key
            return kwargs
        elif isinstance(search_key_name, str):
            draft = {search_key_name : kwargs[search_key_name]}
        elif search_key_name is None:
            return {}
        else:
            draft = dict((k, kwargs[k]) for k in search_key_name)

        for k, v in kwargs.items():
            if k.startswith("return"):
                draft[k] = v

        return draft

    @classmethod
    def find(cls, entity=None, search_key_name='id', **kwargs):
        """
        Looks for an existing object in CiviCRM with parameter search_key_name
        equal to the value for search_key_name specified in kwargs. Returns an
        object of class cls populated with this object's data if found, otherwise
        returns None.
        """
        search_query = cls._search_query(search_key_name, kwargs)
        response = cls._get(entity, **search_query)
        if response['count'] == 0:
            return
        else:
            value = get_unique(response)
            return cls(value)

    @classmethod
    def find_and_update(cls, entity=None, search_key_name='id', **kwargs):
        """
        Looks for an existing object in CiviCRM with parameter search_key_name
        equal to the value for search_key_name specified in kwargs. If a unique
        record is found, record is also updated with additional values in kwargs.

        Returns an object of class cls populated with this object's data if
        found, otherwise returns None.
        """
        search_query = cls._search_query(search_key_name, kwargs)
        response = cls._get(entity, **search_query)
        if response['count'] == 0:
            return
        else:
            value = get_unique(response)
            value.update(kwargs) 
            new_response = cls._create(entity=entity, **value)
            updated_value = get_unique(new_response)
            # not all fields are included in the return from an update, so we merge both sources
            updated_value.update(value)
            return cls(updated_value)

    @classmethod
    def find_all(cls, entity=None, search_key_name='id', **kwargs):
        """
        Looks for multiple existing objects in CiviCRM with parameter
        search_key_name equal to the value for search_key_name specified in
        kwargs. Returns a list of objects of class cls populated with data.
        Returns an empty list if no matching values found.
        """
        search_query = cls._search_query(search_key_name, kwargs)
        response = cls._get(entity, **search_query)
        return [cls(v) for v in response['values']]

    @classmethod
    def create(cls, entity=None, **kwargs):
        response = cls._create(entity, **kwargs)
        logger.debug("new record created! full response: %s" % str(response))
        if not isinstance(response.get('values'), int):
            value = get_unique(response)
            return cls(value)
        else:
            return response

    @classmethod
    def find_or_create(cls, entity=None, search_key_name='id', do_update=False, **kwargs):
        """
        Looks for an existing object in CiviCRM with parameter
        search_key_name equal to the value for search_key_name
        specified in kwargs. Returns this object if it exists,
        otherwise creates a new object.
        """
        if do_update:
            obj = cls.find_and_update(entity=entity, search_key_name=search_key_name, **kwargs)
        else:
            obj = cls.find(entity=entity, search_key_name=search_key_name, **kwargs)

        if obj is None:
            return cls.create(entity, **kwargs)
        else:
            return obj

    def update(self, **kwargs):
        self.civi.update(kwargs)
        kwargs['id'] = self.civi_id
        self.__class__._create(**kwargs)

    def __init__(self, data):
        self.civi = data

    def __repr__(self):
        label = None

        for field_name in self.REPR_FIELDS:
            if field_name in self.civi:
                label = self.civi[field_name]
                break

        return "<%s %s: %s>" % (self.__class__.__name__, self.civi_id, label)

    def pprint(self):
        print(json.dumps(self.civi, sort_keys=True, indent=4))

    def __getattr__(self, key):
        if key in self.civi:
            return self.civi[key]
        elif key.startswith("civi_"):
            return self.civi[key[5:]]

    def __setattr__(self, key, value):
        if key == 'civi':
            object.__setattr__(self, key, value)
        elif key in self.civi:
            self.civi[key] = value
        elif key.startswith("civi_"):
            adj_key = key[5:]
            self.civi[adj_key] = value
        else:
            object.__setattr__(self, key, value)
