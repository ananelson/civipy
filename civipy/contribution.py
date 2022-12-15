from civipy.base import CiviCRMBase
from civipy.base import get_unique
from civipy.contact import CiviContact
from civipy.exceptions import NonUniqueSelectorException


class CiviContribution(CiviCRMBase):
    civicrm_entity_table = 'contribution'

    def complete_transaction(self, **kwargs):
        """
        Calls the CiviCRM API completetransaction action and returns parsed JSON on success.
        """
        kwargs["id"] = self.civi_id
        response = self._post_method()("completetransaction", None, kwargs)
        if not isinstance(response.get("values"), int):
            value = get_unique(response)
            return self.__class__(value)
        else:
            return response

    @classmethod
    def find_by_transaction_id(cls, trxn_id: str):
        """
        Find a contribution by payment transaction ID
        """
        found = cls._get(trxn_id=trxn_id)
        if not found or found.get("count") == 0:
            return
        if found and found.get("count") == 1:
            return cls(get_unique(found))
        raise NonUniqueSelectorException(f"Multiple Civi contribution records found for Payment ID {trxn_id}!")

    @classmethod
    def find_by_invoice_id(cls, invoice_id: str):
        found = cls._get(invoice_id=invoice_id)
        if not found or found.get("count") == 0:
            return
        if found and found.get("count") == 1:
            return cls(get_unique(found))
        raise NonUniqueSelectorException(f"Multiple Civi contribution records found for Invoice ID {invoice_id}!")

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
            raise NonUniqueSelectorException(f"Multiple donors named {display_name}")
        contact_obj = get_unique(result)
        return cls.find_by_donor_id(contact_obj["contact_id"], total_amount, receive_date)

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
        return cls.find(**query)


class CiviContributionRecur(CiviCRMBase):
    civicrm_entity_table = 'contributionrecur'

    @classmethod
    def find_by_transaction_id(cls, trxn_id: str):
        """
        Find a recurring contribution by subscription transaction ID
        """
        found = cls._get(trxn_id=trxn_id)
        if not found or found.get("count") == 0:
            return
        if found and found.get("count") == 1:
            return cls(get_unique(found))
        raise NonUniqueSelectorException(f"Multiple ContributionRecur records found for Subscription ID {trxn_id}!")
