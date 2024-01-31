from civipy.base.base import CiviCRMBase
from civipy.base.config import logger


class CiviCountry(CiviCRMBase):
    civicrm_entity_table = "country"

    @classmethod
    def find_by_country_code(cls, country_code: str, select: list[str] | None = None):
        return cls.find(select=select, iso_code=country_code)


class CiviStateProvince(CiviCRMBase):
    pass


class CiviLocationType(CiviCRMBase):
    pass


class CiviAddress(CiviCRMBase):
    country_iso_code_cache = {}
    state_province_abbreviation_cache = {}

    @classmethod
    def create(cls, **kwargs):
        """Calls the CiviCRM API create action and returns parsed JSON on success.

        Accepts field country_iso_code and will convert this to country_id
        Accepts field state_province_abbreviation and will convert this to state_province_id"""
        if "country_iso_code" in kwargs:
            country_iso_code = kwargs["country_iso_code"]
            del kwargs["country_iso_code"]
            if country_iso_code in cls.country_iso_code_cache:
                country = cls.country_iso_code_cache[country_iso_code]
            else:
                country = CiviCountry.find_by_country_code(country_iso_code)
                cls.country_iso_code_cache[country_iso_code] = country

            kwargs["country_id"] = country.civi_id

            if country.civi_id not in cls.state_province_abbreviation_cache:
                cls.state_province_abbreviation_cache[country.civi_id] = {}

            if "state_province_abbreviation" in kwargs:
                abbreviation = kwargs["state_province_abbreviation"]
                del kwargs["state_province_abbreviation"]
                if country.is_province_abbreviated:
                    if abbreviation in cls.state_province_abbreviation_cache[country.civi_id]:
                        logger.debug("Using cache for %s" % abbreviation)
                        state_province_id = cls.state_province_abbreviation_cache[country.civi_id][abbreviation]
                    else:
                        state_province = CiviStateProvince.find(country_id=country.civi_id, abbreviation=abbreviation)
                        state_province_id = state_province["id"]
                        cls.state_province_abbreviation_cache[country.civi_id][abbreviation] = state_province_id
                    kwargs["state_province_id"] = state_province_id
                else:
                    kwargs["supplemental_address_3"] = abbreviation
        return super().create(**kwargs)
