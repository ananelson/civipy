from civipy.base.base import CiviCRMBase


class CiviNote(CiviCRMBase):
    pass


class CiviNotable(CiviCRMBase):
    def _where_for_note(self, subject: str) -> dict[str, str | int]:
        return {
            "entity_id": self.civi["id"],
            "entity_table": self.__class__.civicrm_entity_table,
            "subject": subject,
        }

    def add_note(self, subject: str, note: str):
        return CiviNote.create(note=note, **self._where_for_note(subject))

    def find_or_create_note(self, subject: str, note: str):
        return CiviNote.find_or_create(where=self._where_for_note(subject), note=note)
