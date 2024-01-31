import json
from typing import TypeVar
from civipy.base.config import logger
from civipy.base.utils import get_unique
from civipy.exceptions import CiviProgrammingError
from civipy.interface import get_interface, CiviValue, CiviResponse, Interface

CiviEntity = TypeVar("CiviEntity", bound="CiviCRMBase")


class CiviCRMBase:
    @classmethod
    def get(cls, **kwargs) -> CiviResponse:
        """Make an API request with the "get" action and return the full response."""
        query = cls._interface().limit(25)
        query.update(kwargs)
        return cls.action("get", **query)

    @classmethod
    def create(cls, **kwargs: CiviValue) -> CiviEntity:
        """Make an API request with the "create" action and return an object of class cls
        populated with the created object's data."""
        query = cls._interface().values(kwargs)
        response = cls.action("create", **query)
        logger.debug("new record created! full response: %s" % str(response))
        return cls(get_unique(response))

    def update(self: CiviEntity, **kwargs: CiviValue) -> CiviResponse:
        """Update the current object with the values specified in kwargs. Returns the full
        API response."""
        self.civi.update(kwargs)
        query = self._interface().where({"id": self.civi_id})
        query.update(self._interface().values(kwargs))
        return self.action("create", **query)

    @classmethod
    def find(cls, select: list[str] | None = None, **kwargs: CiviValue) -> CiviEntity | None:
        """Looks for an existing object in CiviCRM with parameters equal to the values
        specified in kwargs. If using API v4 and select is specified, the result will include
        the specified keys.

        Returns an object of class cls populated with this object's data if found, otherwise
        returns None."""
        query = cls._interface().where(kwargs)
        if select:
            query["select"] = select
        response = cls.get(**query)
        if response["count"] == 0:
            return None
        return cls(get_unique(response))

    @classmethod
    def find_all(cls, select: list[str] | None = None, **kwargs: CiviValue) -> list[CiviEntity]:
        """Looks for multiple existing objects in CiviCRM with parameters equal to the
        values specified in kwargs. If using API v4 and select is specified, the result will
        include the specified keys.

        Returns a list of objects of class cls populated with data. Returns an empty list
        if no matching values found."""
        query = cls._interface().where(kwargs)
        if select:
            query["select"] = select
        response = cls.action("get", **query)
        return [cls(v) for v in response["values"]]

    @classmethod
    def find_and_update(cls, where: CiviValue, **kwargs: CiviValue) -> CiviEntity | None:
        """Looks for an existing object in CiviCRM with parameters equal to the values
        specified in `where`.

        If a unique record is found, record is also updated with values in `kwargs`.

        Returns an object of class cls populated with this object's data if found, otherwise
        returns None."""
        query = cls._interface().where(where)
        response = cls.get(**query)
        if response["count"] == 0:
            return None

        value = get_unique(response)
        value.update(kwargs)
        new_response = cls.action("create", **value)
        updated_value = get_unique(new_response)
        # not all fields are included in the return from an update, so we merge both sources
        updated_value.update(value)
        return cls(updated_value)

    @classmethod
    def find_or_create(cls, where: CiviValue, do_update: bool = False, **kwargs: CiviValue) -> CiviEntity:
        """Looks for an existing object in CiviCRM with parameters search_keys equal to the
        values for search_keys specified in kwargs.

        If a unique record is found and do_update is True, record is also updated with
        values in `kwargs`.

        If no record is found, a new record is created with the data in `where` and `kwargs`.

        Returns an object of class cls populated with the found, updated, or created
        object's data."""
        if do_update:
            obj = cls.find_and_update(where, **kwargs)
        else:
            obj = cls.find(**kwargs)

        if obj is None:
            query = where.copy()
            query.update(kwargs)
            return cls.create(**query)
        return obj

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
        """Instantiate the appropriate API interface and store it on the CiviCRMBase class,
        so that it will be instantiated only once and available to all entity classes."""
        if CiviCRMBase._interface_reference is None:
            CiviCRMBase._interface_reference = get_interface()
        return CiviCRMBase._interface_reference

    def pprint(self: CiviEntity) -> None:
        """Print the current record's data in a human-friendly format."""
        print(json.dumps(self.civi, sort_keys=True, indent=4))

    def __init__(self: CiviEntity, data: CiviValue) -> None:
        self.civi = data

    REPR_FIELDS = ["display_name", "name"]

    def __repr__(self: CiviEntity):
        label = None

        for field_name in self.REPR_FIELDS:
            if field_name in self.civi:
                label = self.civi[field_name]
                break

        return f"<{self.__class__.__name__} {self.civi_id}: {label}>"

    def __getattr__(self: CiviEntity, key: str):
        if key in self.civi:
            return self.civi[key]
        elif key.startswith("civi_"):
            return self.civi[key[5:]]
        return object.__getattribute__(self, key)

    def __setattr__(self: CiviEntity, key: str, value: str | int | None) -> None:
        if key == "civi":
            object.__setattr__(self, key, value)
        elif key in self.civi:
            self.civi[key] = value
        elif key.startswith("civi_"):
            adj_key = key[5:]
            self.civi[adj_key] = value
        else:
            object.__setattr__(self, key, value)
