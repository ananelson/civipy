from civipy.base.base import CiviCRMBase
from civipy.activity import CiviActivity, CiviActivityContact
from civipy.address import CiviAddress, CiviLocationType, CiviStateProvince, CiviCountry
from civipy.contact import CiviContact, CiviEmail, CiviPhone, CiviRelationship, CiviTag, CiviEntityTag, CiviWebsite
from civipy.contact import CiviGroup, CiviGroupContact
from civipy.contribution import CiviContribution, CiviContributionRecur
from civipy.event import CiviEvent, CiviParticipant
from civipy.financial import CiviEntityFinancialTrxn
from civipy.grant import CiviGrant
from civipy.mailing import CiviMailingEventQueue
from civipy.membership import CiviMembership, CiviMembershipPayment
from civipy.note import CiviNote
from civipy.option_group import CiviCustomField, CiviCustomValue, CiviOptionGroup, CiviOptionValue
from civipy.order import CiviOrder, CiviPayment
from civipy.user import CiviUFField, CiviUFGroup, CiviUFJoin, CiviUFMatch, CiviUser

# enable e.g.
# >>> import civipy
# >>> civipy.init(rest_base="", ...)
from civipy.base.config import SETTINGS

init = SETTINGS.init
del SETTINGS
__all__ = [
    "CiviActivity",
    "CiviActivityContact",
    "CiviAddress",
    "CiviContact",
    "CiviContribution",
    "CiviContributionRecur",
    "CiviCountry",
    "CiviCustomField",
    "CiviCustomValue",
    "CiviEmail",
    "CiviEntityFinancialTrxn",
    "CiviEntityTag",
    "CiviEvent",
    "CiviGrant",
    "CiviGroup",
    "CiviGroupContact",
    "CiviLocationType",
    "CiviMailingEventQueue",
    "CiviMembership",
    "CiviMembershipPayment",
    "CiviNote",
    "CiviOptionGroup",
    "CiviOptionValue",
    "CiviOrder",
    "CiviParticipant",
    "CiviPayment",
    "CiviPhone",
    "CiviRelationship",
    "CiviStateProvince",
    "CiviTag",
    "CiviUFField",
    "CiviUFGroup",
    "CiviUFJoin",
    "CiviUFMatch",
    "CiviUser",
    "CiviWebsite",
    "CiviCRMBase",
    "init",
]
