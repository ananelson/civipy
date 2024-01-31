from civipy.base.base import CiviCRMBase
from civipy.base.base import get_unique
from civipy.contact import CiviContact


class CiviContribution(CiviCRMBase):
    civicrm_entity_table = "contribution"

    def complete_transaction(self, **kwargs):
        """Calls the CiviCRM API completetransaction action and returns parsed JSON on success."""
        kwargs["id"] = self.civi_id
        response = self.action("completetransaction", **kwargs)
        if not isinstance(response.get("values"), int):
            value = get_unique(response)
            return self.__class__(value)
        else:
            return response

    @classmethod
    def find_by_transaction_id(cls, trxn_id: str, select: list[str] | None = None):
        """Find a contribution by payment transaction ID"""
        return cls.find(select=select, trxn_id=trxn_id)

    @classmethod
    def find_by_invoice_id(cls, invoice_id: str, select: list[str] | None = None):
        return cls.find(select=select, invoice_id=invoice_id)

    @classmethod
    def find_by_donor(
        cls,
        display_name: str,
        total_amount: float | None = None,
        receive_date: str | None = None,
        select: list[str] | None = None,
    ):
        """Find a contribution by donor's display name, and optionally
        by amount and/or date received (yyyy-mm-dd)."""
        contact = CiviContact.find(select=["contact_id"], display_name=display_name)
        return cls.find_by_donor_id(contact["contact_id"], total_amount, receive_date, select)

    @classmethod
    def find_by_donor_id(
        cls,
        contact_id: int,
        total_amount: float | None = None,
        receive_date: str | None = None,
        select: list[str] | None = None,
    ):
        """Find a contribution by donor's contact ID, and optionally
        by amount and/or date received (yyyy-mm-dd)."""
        query = {"contact_id": contact_id}
        if total_amount is not None:
            query["total_amount"] = total_amount
        if receive_date is not None:
            query["receive_date"] = {"BETWEEN": [receive_date, f"{receive_date} 23:59:59"]}
        return cls.find(select=select, **query)


class CiviContributionRecur(CiviCRMBase):
    civicrm_entity_table = "contributionrecur"

    @classmethod
    def find_by_transaction_id(cls, trxn_id: str, select: list[str] | None = None):
        """
        Find a recurring contribution by subscription transaction ID
        """
        return cls.find(select=select, trxn_id=trxn_id)
