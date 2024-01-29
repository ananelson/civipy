import json
from civipy.base.base import CiviCRMBase
from civipy.exceptions import CiviProgrammingError
from civipy.note import CiviNotable


class CiviContact(CiviNotable):
    civicrm_entity_table = "contact"

    @classmethod
    def find_by_email(cls, email_address):
        email_obj = CiviEmail.find(email=email_address)
        return cls.find(id=email_obj["contact_id"])


class CiviEmail(CiviCRMBase):
    pass


class CiviPhone(CiviCRMBase):
    pass


class CiviWebsite(CiviCRMBase):
    pass


class CiviRelationship(CiviCRMBase):
    @classmethod
    def create_or_increment_relationship(
        cls,
        contact_id_a: int,
        contact_id_b: int,
        relationship_type_id: int,
        event_id: int | None = None,
        activity_id: int | None = None,
    ):
        print(f"in create_or_increment_relationship with a {contact_id_a} b {contact_id_b} type {relationship_type_id}")
        if not event_id and not activity_id:
            raise CiviProgrammingError("Must provide either event_id or activity_id")

        existing_relationship = cls.find(
            contact_id_a=contact_id_a,
            contact_id_b=contact_id_b,
            relationship_type_id=relationship_type_id,
        )
        if existing_relationship is None:
            # look for reverse relationship
            existing_relationship = cls.find(
                contact_id_a=contact_id_b,
                contact_id_b=contact_id_a,
                relationship_type_id=relationship_type_id,
            )

        events = [event_id] if event_id else []
        activities = [activity_id] if activity_id else []
        if existing_relationship is None:
            # create new relationship
            cls.create(
                contact_id_a=contact_id_a,
                contact_id_b=contact_id_b,
                relationship_type_id=relationship_type_id,
                description=json.dumps({"events": events, "activities": activities}),
                debug=1,
            )
        else:
            # update existing relationship
            relationship_info = {}
            if "description" in existing_relationship.civi:
                desc = existing_relationship.civi_description
                try:
                    relationship_info = json.loads(desc)
                except json.decoder.JSONDecodeError:
                    pass

            if "events" not in relationship_info:
                events.extend(relationship_info["events"])
            relationship_info["events"] = list(set(filter(None, events)))

            if "activities" not in relationship_info:
                activities.extend(relationship_info["activities"])
            relationship_info["activities"] = list(set(filter(None, activities)))

            existing_relationship.update(description=json.dumps(relationship_info))


class CiviEntityTag(CiviCRMBase):
    pass


class CiviTag(CiviCRMBase):
    pass


class CiviGroupContact(CiviCRMBase):
    pass


class CiviGroup(CiviCRMBase):
    @classmethod
    def find_by_title(cls, title: str) -> "CiviGroup":
        """Creates a new CiviGroup object populated with data for the group entitled "title"."""
        return cls.find(title=title)

    def add_member(self, civi_contact: CiviContact) -> CiviGroupContact:
        return CiviGroupContact.find_or_create(contact_id=civi_contact.civi["id"], group_id=self.civi["id"])
