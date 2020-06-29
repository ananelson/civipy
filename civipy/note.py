from civipy.base import CiviCRMBase

class CiviActivity(CiviCRMBase):
    pass

class CiviNote(CiviCRMBase):
    pass

class CiviNotable(CiviCRMBase):
    def _kwargs_for_note(self, subject, note):
        return {
                'entity_id' : self.civi['id'],
                'entity_table' : self.__class__.civicrm_entity_table,
                'subject' : subject,
                'note' : note
                }

    def add_note(self, subject, note):
        CiviNote.create(**self._kwargs_for_note(subject, note))

    def find_or_create_note(self, subject, note):
        CiviNote.find_or_create(search_key_name = ['entity_id', 'entity_table', 'subject'], **self._kwargs_for_note(subject, note))
