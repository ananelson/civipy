from civipy.base import CiviCRMBase
from civipy.base import get_unique_value

class CiviCustomValue(CiviCRMBase):
    pass

class CiviCustomField(CiviCRMBase):
    @classmethod
    def find_field_by_label(klass, field_label):
        response = CiviCustomField._get(label=field_label)
        field = get_unique_value(response)
        return field
