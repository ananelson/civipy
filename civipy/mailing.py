from civipy.base.base import CiviCRMBase
from civipy.exceptions import NonUniqueResultError


class CiviMailingEventQueue(CiviCRMBase):
    """This is the table that links CiviMail mailings to Contacts.

    Attributes:
        id: str e.g. "1202"
        job_id: str e.g. "27"
        email_id: str e.g. "96173"
        hash: str e.g. "1fc2d50bfafd5c27"
        contact_id: str e.g. "16257"
    """

    @classmethod
    def find_recipients(cls, contact_ids: list[int]) -> "CiviMailingEventQueue | None":
        result = []
        for contact_id in set(contact_ids):
            found = cls.find_all(contact_id=contact_id)
            if not found:
                continue
            result.append(found[0])
        if not result:
            return None
        if len(result) != 1:
            raise NonUniqueResultError("Too many results")
        result = result[0]
        for attr in ("id", "job_id", "email_id", "contact_id"):
            if attr in result.civi:
                result.civi[attr] = int(result.civi[attr])
        return result
