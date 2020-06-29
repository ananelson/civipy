from civipy.base import CiviCRMBase
from civipy.note import CiviNotable
from civipy.base import get_unique
import json

class CiviContact(CiviNotable):
    civicrm_entity_table = 'contact'

    @classmethod
    def find_by_email(klass, email_address):
        result = CiviEmail._get(email=email_address)
        if result['count'] == 0:
            return None
        elif result['count'] > 1:
            print(result)
            raise Exception("multiple emails found for %s" % email_address)
        else:
            email_obj = get_unique(result)
            return CiviContact.find(**{"id" : email_obj['contact_id']})

class CiviEmail(CiviCRMBase):
    pass

class CiviPhone(CiviCRMBase):
    pass

class CiviWebsite(CiviCRMBase):
    pass

class CiviRelationship(CiviCRMBase):
    @classmethod
    def create_or_increment_relationship(klass, contact_id_a, contact_id_b, relationship_type_id, event_id=None, activity_id=None):
        print("in create_or_increment_relationship with a %s b %s type %s" % (contact_id_a, contact_id_b, relationship_type_id))

        if not event_id and not activity_id:
            raise Exception("must provide either event_id or activity_id")

        existing_relationship = klass.find(
                search_key_name = ['contact_id_a', 'contact_id_b', 'relationship_type_id'],
                contact_id_a = contact_id_a,
                contact_id_b = contact_id_b,
                relationship_type_id = relationship_type_id)

        if existing_relationship is None:
            # look for reverse relationship
            existing_relationship = klass.find(
                    search_key_name = ['contact_id_a', 'contact_id_b', 'relationship_type_id'],
                    contact_id_a = contact_id_b,
                    contact_id_b = contact_id_a,
                    relationship_type_id = relationship_type_id)

        events = []
        activities = []
        if event_id:
            events.append(event_id)
        if activity_id:
            activities.append(activity_id)

        if existing_relationship is None:
            # create new relationshp
            klass.create(
                contact_id_a = contact_id_a,
                contact_id_b = contact_id_b,
                relationship_type_id = relationship_type_id,
                description = json.dumps({"events" : events, "activities" : activities}),
                debug=1
                )
        else:
            # update existing relationshp
            if 'description' in existing_relationship.civi:
                desc = existing_relationship.civi_description
                try:
                    relationship_info = json.loads(desc)
                except json.decoder.JSONDecodeError:
                    relationship_info = None

            if not relationship_info:
                relationship_info = {}
            if not 'events' in relationship_info:
                relationship_info['events'] = []
            if not 'activities' in relationship_info:
                relationship_info['activities'] = []

            relationship_info['events'].extend(events)
            relationship_info['activities'].extend(activities)

            relationship_info['events'] = list(set(e for e in relationship_info['events'] if e))
            relationship_info['activities'] = list(set(e for e in relationship_info['activities'] if e))

            existing_relationship.update(description=json.dumps(relationship_info))

class CiviTag(CiviCRMBase):
    pass

class CiviGroupContact(CiviCRMBase):
    pass

class CiviGroup(CiviCRMBase):
    @classmethod
    def find(klass, title):
        """
        Creates a new CiviGroup object populated with 
        data for the group entitled "title"
        """
        response = CiviGroup._get(title=title)
        group_data = get_unique(response)
        return klass(group_data)

    def add_member(self, civi_contact):
        CiviGroupContact.find_or_create(
                search_key_name = ['contact_id', 'group_id'],
                contact_id = civi_contact.civi['id'],
                group_id = self.civi['id']
                )
