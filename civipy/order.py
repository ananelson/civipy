from civipy.base import CiviCRMBase

class CiviOrder(CiviCRMBase):
    pass

class CiviPayment(CiviCRMBase):
    @classmethod
    def cancel(cls, **kwargs):
        return cls._post_method()('cancel', "Payment", kwargs)
