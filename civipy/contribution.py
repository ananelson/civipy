from civipy.base import CiviCRMBase
from civipy.base import get_unique
from civipy.contact import CiviContact
from civipy.exceptions import NonUniqueNameException


class CiviContribution(CiviCRMBase):
    civicrm_entity_table = 'contribution'

    @classmethod
    def find_by_transaction_id(cls, trxn_id: str):
        """
        Find a contribution by payment transaction ID
        """
        return cls.find(search_key_name="trxn_id", trxn_id=trxn_id)

    @classmethod
    def find_by_donor(cls, display_name: str, total_amount=None, receive_date=None):
        """
        Find a contribution by donor's display name, and optionally
        by amount and/or date received (yyyy-mm-dd).
        """
        result = CiviContact._get(display_name=display_name)
        if result["count"] == 0:
            return
        elif result["count"] > 1:
            raise NonUniqueNameException(f"Multiple donors named {display_name}")
        contact_obj = get_unique(result)
        return CiviContribution.find_by_donor_id(
            contact_obj["contact_id"], total_amount, receive_date
        )

    @classmethod
    def find_by_donor_id(cls, contact_id: int, total_amount=None, receive_date=None):
        """
        Find a contribution by donor's contact ID, and optionally
        by amount and/or date received (yyyy-mm-dd).
        """
        query = {"contact_id": contact_id}
        if total_amount is not None:
            query["total_amount"] = total_amount
        if receive_date is not None:
            query["receive_date"] = {
                "BETWEEN": [receive_date, f"{receive_date} 23:59:59"]
            }
        return cls.find_all(search_key_name=query.keys(), **query)


class CiviContributionRecur(CiviCRMBase):
    civicrm_entity_table = 'contributionrecur'

