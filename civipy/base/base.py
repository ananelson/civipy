import json
from civipy.base.config import logger
from civipy.base.utils import get_unique
from civipy.exceptions import CiviProgrammingError
from civipy.interface import get_interface, CiviValue, CiviResponse, Interface


class CiviCRMBase:
    ###################################
    # Common API Read Action methods  #
    ###################################
    @classmethod
    def get(cls, **kwargs) -> CiviResponse:
        return cls.action("get", **kwargs)

    ###################################
    # Common API Write Action methods #
    ###################################
    @classmethod
    def create(cls, **kwargs):
        response = cls.action("create", **kwargs)
        logger.debug("new record created! full response: %s" % str(response))
        if not isinstance(response.get("values"), int):
            value = get_unique(response)
            return cls(value)
        else:
            return response

    def update(self, **kwargs):
        self.civi.update(kwargs)
        kwargs["id"] = self.civi_id
        self.action("create", **kwargs)

    ##############################
    # Common convenience methods #
    ##############################
    @classmethod
    def find(cls, search_key: str | list[str] = "id", **kwargs) -> CiviValue | None:
        """Looks for an existing object in CiviCRM with parameter search_key
        equal to the value for search_key specified in kwargs. Returns an
        object of class cls populated with this object's data if found, otherwise
        returns None."""
        search_query = cls._interface().search_query(search_key, kwargs)
        response = cls.action("get", **search_query)
        if response["count"] == 0:
            return None
        return cls(get_unique(response))

    @classmethod
    def find_and_update(cls, search_key: str | list[str] = "id", **kwargs):
        """Looks for an existing object in CiviCRM with parameter search_key
        equal to the value for search_key specified in kwargs. If a unique
        record is found, record is also updated with additional values in kwargs.

        Returns an object of class cls populated with this object's data if
        found, otherwise returns None."""
        search_query = cls._interface().search_query(search_key, kwargs)
        response = cls.action("get", **search_query)
        if response["count"] == 0:
            return
        else:
            value = get_unique(response)
            value.update(kwargs)
            new_response = cls.action("create", **value)
            updated_value = get_unique(new_response)
            # not all fields are included in the return from an update, so we merge both sources
            updated_value.update(value)
            return cls(updated_value)

    @classmethod
    def find_all(cls, search_key: str | list[str] = "id", **kwargs):
        """Looks for multiple existing objects in CiviCRM with parameter
        search_key equal to the value for search_key specified in
        kwargs. Returns a list of objects of class cls populated with data.
        Returns an empty list if no matching values found."""
        search_query = cls._interface().search_query(search_key, kwargs)
        response = cls.action("get", **search_query)
        return [cls(v) for v in response["values"]]

    @classmethod
    def find_or_create(cls, search_key: str | list[str] = "id", do_update: bool = False, **kwargs):
        """Looks for an existing object in CiviCRM with parameter
        search_key equal to the value for search_key
        specified in kwargs. Returns this object if it exists,
        otherwise creates a new object."""
        if do_update:
            obj = cls.find_and_update(search_key=search_key, **kwargs)
        else:
            obj = cls.find(search_key=search_key, **kwargs)

        if obj is None:
            return cls.create(**kwargs)
        else:
            return obj

    #############################
    # Direct API access methods #
    #############################
    @classmethod
    def action(cls, action: str, **kwargs) -> CiviResponse:
        """Calls the CiviCRM API action and returns parsed JSON on success."""
        entity = cls.__name__[4:]
        if entity == "CRMBase":
            raise CiviProgrammingError("Subclass CiviCRMBase to create an unsupported Entity.")
        return cls._interface()(action, entity, kwargs)

    _interface_reference: Interface | None = None

    @classmethod
    def _interface(cls) -> Interface:
        if cls._interface_reference is None:
            cls._interface_reference = get_interface()
        return cls._interface_reference

    ############################
    # Instance support methods #
    ############################
    def pprint(self):
        print(json.dumps(self.civi, sort_keys=True, indent=4))

    def __init__(self, data: CiviValue):
        self.civi = data

    REPR_FIELDS = ["display_name", "name"]

    def __repr__(self):
        label = None

        for field_name in self.REPR_FIELDS:
            if field_name in self.civi:
                label = self.civi[field_name]
                break

        return f"<{self.__class__.__name__} {self.civi_id}: {label}>"

    def __getattr__(self, key: str):
        if key in self.civi:
            return self.civi[key]
        elif key.startswith("civi_"):
            return self.civi[key[5:]]
        return object.__getattribute__(self, key)

    def __setattr__(self, key: str, value: str | int | None):
        if key == "civi":
            object.__setattr__(self, key, value)
        elif key in self.civi:
            self.civi[key] = value
        elif key.startswith("civi_"):
            adj_key = key[5:]
            self.civi[adj_key] = value
        else:
            object.__setattr__(self, key, value)
