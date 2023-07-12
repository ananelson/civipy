from civipy.base import CiviCRMBase


class CiviUFField(CiviCRMBase):
    ...


class CiviUFGroup(CiviCRMBase):
    ...


class CiviUFJoin(CiviCRMBase):
    ...


class CiviUFMatch(CiviCRMBase):
    """This is the table that matches WordPress users to CiviCRM Contacts.

    create requires uf_id, uf_name, and contact_id

    Attributes:
        id: str e.g. "24392"
        domain_id: str e.g. "1"
        uf_id: str e.g. "46914"
        uf_name: str e.g. "user@example.com"
        contact_id: str e.g. "367872"
    """

    @classmethod
    def find_wp(cls, contact_ids):
        result = []
        for contact_id in set(contact_ids):
            found = cls.find(search_key_name="contact_id", contact_id=contact_id)
            if not found:
                continue
            result.append(found)
        if not result:
            raise ValueError("No result found!")
        if len(result) != 1:
            views = [f"{r.civi}\n" for r in result]
            raise ValueError(f"Too many results:\n {''.join(views)}")
        result = result[0]
        for attr in ("id", "domain_id", "uf_id", "contact_id"):
            result.civi[attr] = int(result.civi[attr])
        return result

    def update_wp_user(self, wp_user_id):
        payload = self.civi
        payload["uf_id"] = wp_user_id
        self.update(**payload)


class CiviUser(CiviCRMBase):
    ...
