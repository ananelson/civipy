from civipy.base import CiviCRMBase
from civipy.base import get_unique


class CiviOptionValue(CiviCRMBase):
    pass

class CiviOptionGroup(CiviCRMBase):
    @classmethod
    def find_options_by_group_name(klass, option_group_name):
        """
        Taking an option_group_name, looks up the group and its members.
        """
        response = CiviOptionGroup._get(name=option_group_name)
        og = get_unique(response)
        values_response = CiviOptionValue._get(option_group_id = og['id'])
        return values_response['values']

    @classmethod
    def option_values_dict_by_group_name(klass, option_group_name):
        """
        Taking an option_group_name, looks up the group and its members.
        """
        option_values_list = klass.find_options_by_group_name(option_group_name)
        if isinstance(option_values_list, dict):
            option_values_list = option_values_list.values()
        return dict((t['name'], t['value']) for t in option_values_list)

class CiviCustomValue(CiviCRMBase):
    pass

class CiviCustomField(CiviCRMBase):
    @classmethod
    def find_field_by_label(klass, field_label):
        response = CiviCustomField._get(label=field_label)
        field = get_unique(response)
        return field

    @classmethod
    def find_options_by_field_label(klass, label):
        custom_field = klass.find(label=label)
        values_response = CiviOptionValue._get(option_group_id = custom_field.civi_option_group_id)
        return values_response['values']

    @classmethod
    def options_label_map(klass, label):
        option_values = klass.find_options_by_field_label(label)
        return dict((ov['label'], ov['value']) for ov in option_values)
