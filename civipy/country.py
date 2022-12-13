from civipy.base import CiviCRMBase
from civipy.base import get_unique
from civipy.exceptions import NonUniqueSelectorException


class CiviCountry(CiviCRMBase):
    civicrm_entity_table = "country"

    @classmethod
    def find_by_country_code(cls, country_code: str):
        found = cls._get(iso_code=country_code)
        if not found or found.get("count") == 0:
            return
        if found and found.get("count") == 1:
            return cls(get_unique(found))
        raise NonUniqueSelectorException(f"Multiple Civi country records found for Country ISO Code {country_code}!")
