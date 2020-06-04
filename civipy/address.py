from civipy.base import CiviCRMBase
from civipy.base import get_unique_value
from civipy.config import logger

class CiviStateProvince(CiviCRMBase):
    pass

class CiviCountry(CiviCRMBase):
    pass

class CiviAddress(CiviCRMBase):
    country_iso_code_cache = {}
    state_province_abbreviation_cache = {}

    @classmethod
    def _create(klass, entity=None, **kwargs):
        """
        Calls the CiviCRM API create action and returns parsed JSON on success.

        Accepts field country_iso_code and will convert this to country_id
        Accepts field state_province_abbreviation and will convert this to state_province_id
        """
        if 'country_iso_code' in kwargs:
            country_iso_code = kwargs['country_iso_code']
            if country_iso_code in klass.country_iso_code_cache:
                country_id = klass.country_iso_code_cache[country_iso_code]
            else:
                response = CiviCountry._get(**{"iso_code" : country_iso_code})
                country = get_unique_value(response)
                country_id = country['id']
                klass.country_iso_code_cache[country_iso_code] = country_id

            del kwargs['country_iso_code']
            kwargs['country_id'] = country_id

            if not country_id in klass.state_province_abbreviation_cache:
                klass.state_province_abbreviation_cache[country_id] = {}

        if 'state_province_abbreviation' in kwargs:
            state_province_abbreviation = kwargs['state_province_abbreviation']
            if state_province_abbreviation in klass.state_province_abbreviation_cache[country_id]:
                logger.debug("using cache for %s" % state_province_abbreviation)
                state_province_id = klass.state_province_abbreviation_cache[country_id][state_province_abbreviation]
            else:
                response = CiviStateProvince._get(**{"country_id" : country_id, "abbreviation" : state_province_abbreviation})
                state_province_id = get_unique_value(response)['id']
                klass.state_province_abbreviation_cache[country_id][state_province_abbreviation] = state_province_id

            del kwargs['state_province_abbreviation']
            kwargs['state_province_id'] = state_province_id

        assert 'state_province_id' in kwargs
        assert 'country_id' in kwargs
        return CiviCRMBase.http_post("create", 'Address', kwargs)
