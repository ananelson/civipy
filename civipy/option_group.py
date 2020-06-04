from civipy.base import CiviCRMBase
from civipy.base import get_unique_value

class CiviOptionValue(CiviCRMBase):
    pass

class CiviOptionGroup(CiviCRMBase):
    @classmethod
    def find_options_by_group_name(klass, option_group_name):
        """
        Taking an option_group_name, looks up the group and its members.
        """
        response = CiviOptionGroup._get(name=option_group_name)
        og = get_unique_value(response)
        values_response = CiviOptionValue._get(option_group_id = og['id'])
        return values_response['values']

    @classmethod
    def option_values_dict_by_group_name(klass, option_group_name):
        """
        Taking an option_group_name, looks up the group and its members.
        """
        option_values_list = klass.find_options_by_group_name(option_group_name)
        return dict((t['name'], t['value']) for t in option_values_list)
