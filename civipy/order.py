from civipy.base import CiviCRMBase

class CiviOrder(CiviCRMBase):
    pass

class CiviPayment(CiviCRMBase):
    @classmethod
    def cancel(klass, **kwargs):
        return klass._post_method()('cancel', "Payment", kwargs)
