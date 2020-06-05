from civipy.base import CiviCRMBase
from civipy.base import get_unique_value

class CiviContact(CiviCRMBase):
    pass

class CiviEmail(CiviCRMBase):
    pass

class CiviPhone(CiviCRMBase):
    pass

class CiviWebsite(CiviCRMBase):
    pass

class CiviGroupContact(CiviCRMBase):
    pass

class CiviGroup(CiviCRMBase):
    @classmethod
    def find(klass, title):
        """
        Creates a new CiviGroup object populated with 
        data for the group entitled "title"
        """
        response = CiviGroup._get(title=title)
        group_data = get_unique_value(response)
        return klass(group_data)

    def add_member(self, civi_contact):
        CiviGroupContact.find_or_create(
                contact_id = civi_contact.civi['id'],
                group_id = self.civi['id']
                )
