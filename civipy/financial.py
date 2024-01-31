from civipy.base.base import CiviCRMBase


class CiviEntityFinancialTrxn(CiviCRMBase):
    @classmethod
    def cancel(cls, **kwargs):
        return cls.action("cancel", **kwargs)

    @classmethod
    def find_by_transaction_id(cls, trxn_id: str) -> "CiviFinancialTrxn | None":
        """Find a Contribution Payment by payment transaction ID"""
        kwargs = {
            "select": ["*", "financial_trxn_id.*"],
            "entity_table": "civicrm_contribution",
            "financial_trxn_id.trxn_id": trxn_id,
        }
        found = cls.find_all(**kwargs)
        return next(filter(lambda c: bool(c.civi.get("entity_id")), found), None)
