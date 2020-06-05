import requests
import json

from civipy.config import REST_BASE
from civipy.config import USER_KEY
from civipy.config import SITE_KEY
from civipy.config import logger

def assert_unique(response):
    if not 'count' in response:
        print(response)
        raise Exception("no count in response!")
    assert response['count'] == 1, response

def get_unique_value(response):
    assert_unique(response)
    return response['values'][0]

class CiviCRMBase(object):
    @classmethod
    def _entity(klass, entity=None):
        if entity is None:
            entity = klass.__name__[4:]
            if entity == "CRMBase":
                raise Exception("Must provide entity")
        return entity

    @classmethod
    def _params(klass, entity, action, kwargs):
        entity = klass._entity(entity)
        json_params = {'sequential' : 1}
        json_params.update(kwargs)
        return {
                'entity' : entity,
                'action' : action,
                'api_key' : USER_KEY,
                'key' : SITE_KEY,
                'json' : json.dumps(json_params)
                }

    @classmethod
    def http_get(klass, action, entity, kwargs):
        params = klass._params(entity, action, kwargs)
        logger.debug(str(params))
        r = requests.get(
                REST_BASE,
                params = params)
        if r.status_code == 200:
            return r.json()

    @classmethod
    def http_post(klass, action, entity, kwargs):
        params = klass._params(entity, action, kwargs)
        logger.debug(str(params))
        r = requests.post(
                REST_BASE,
                params = params)
        if r.status_code == 200:
            return r.json()

    @classmethod
    def _get(klass, entity=None, **kwargs):
        """
        Calls the CiviCRM API get action and returns parsed JSON on success.
        """
        return klass.http_get('get', entity, kwargs)

    @classmethod
    def _getsingle(klass, entity, **kwargs):
        """
        Calls the CiviCRM API getsingle action and returns parsed JSON on success.
        """
        return klass.http_get('getsingle', entity, kwargs)

    @classmethod
    def _create(klass, entity=None, **kwargs):
        """
        Calls the CiviCRM API create action and returns parsed JSON on success.
        """
        return klass.http_post('create', entity, kwargs)


    @classmethod
    def _search_query(klass, search_key_name, kwargs):
        if isinstance(search_key_name, str):
            return {search_key_name : kwargs[search_key_name]}
        else:
            return dict((k, kwargs[k]) for k in search_key_name)

    @classmethod
    def find(klass, entity=None, search_key_name='id', **kwargs):
        """
        Looks for an existing object in CiviCRM with parameter search_key_name
        equal to the value for search_key_name specified in kwargs. Returns an
        object of class klass populated with this object's data if found.
        """
        search_query = klass._search_query(search_key_name, kwargs)
        response = klass._get(entity, **search_query)
        value = get_unique_value(response)
        return klass(value)

    @classmethod
    def find_or_create(klass, entity=None, search_key_name='id', do_update=False, **kwargs):
        """
        Looks for an existing object in CiviCRM with parameter
        search_key_name equal to the value for search_key_name
        specified in kwargs. Returns this object if it exists,
        otherwise creates a new object. Return's object's parsed JSON.
        """
        search_query = klass._search_query(search_key_name, kwargs)
        response = klass._get(entity, **search_query)
        if response['count'] == 1:
            logger.debug("found existing record for: %s" % str(search_query))
            obj = response['values'][0]
            logger.debug(obj)
            if do_update:
                logger.debug("do_update is true, updating record to match: %s" % str(kwargs))
                obj.update(kwargs)
                klass._create(entity, **obj)
            return obj
        else:
            logger.debug("creating new record for %s" % str(kwargs))
            response = klass._create(entity, **kwargs)
            logger.debug("new record created! full response: %s" % str(response))
            assert_unique(response)
            return response['values'][0]

    def __init__(self, data):
        self.civi = data
