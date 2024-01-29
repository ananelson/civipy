from civipy.base.base import CiviCRMBase


class CiviOptionValue(CiviCRMBase):
    pass


class CiviOptionGroup(CiviCRMBase):
    @classmethod
    def find_options_by_group_name(cls, option_group_name: str):
        """
        Taking an option_group_name, looks up the group and its members.
        """
        og = CiviOptionGroup.find(name=option_group_name)
        return CiviOptionValue.find_all(option_group_id=og["id"])

    @classmethod
    def option_values_dict_by_group_name(cls, option_group_name):
        """
        Taking an option_group_name, looks up the group and its members.
        """
        option_values_list = cls.find_options_by_group_name(option_group_name)
        if isinstance(option_values_list, dict):
            option_values_list = option_values_list.values()
        return dict((t["name"], t["value"]) for t in option_values_list)


class CiviCustomValue(CiviCRMBase):
    pass


class CiviCustomField(CiviCRMBase):
    @classmethod
    def find_field_by_label(cls, field_label: str):
        return CiviCustomField.find(label=field_label)

    @classmethod
    def find_options_by_field_label(cls, label: str):
        custom_field = cls.find(label=label)
        return CiviOptionValue.find_all(option_group_id=custom_field.civi_option_group_id)

    @classmethod
    def options_label_map(cls, label: str):
        option_values = cls.find_options_by_field_label(label)
        return dict((ov["label"], ov["value"]) for ov in option_values)
