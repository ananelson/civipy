from civipy.base.base import CiviCRMBase


class CiviOrder(CiviCRMBase):
    pass


class CiviPayment(CiviCRMBase):
    @classmethod
    def cancel(cls, **kwargs):
        return cls.action("cancel", **kwargs)

    @classmethod
    def find_by_transaction_id(cls, trxn_id: str, select: list[str] | None = None) -> "CiviPayment | None":
        """Find a Contribution Payment by payment transaction ID"""
        found = cls.find_all(select=select, trxn_id=trxn_id)
        return next(filter(lambda c: bool(c.civi.get("contribution_id")), found), None)
