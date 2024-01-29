from civipy.base.base import CiviCRMBase


class CiviNote(CiviCRMBase):
    pass


class CiviNotable(CiviCRMBase):
    def _kwargs_for_note(self, subject: str, note: str) -> dict[str, str | int]:
        return {
            "entity_id": self.civi["id"],
            "entity_table": self.__class__.civicrm_entity_table,
            "subject": subject,
            "note": note,
        }

    def add_note(self, subject: str, note: str):
        return CiviNote.create(**self._kwargs_for_note(subject, note))

    def find_or_create_note(self, subject: str, note: str):
        return CiviNote.find_or_create(
            search_key=["entity_id", "entity_table", "subject"], **self._kwargs_for_note(subject, note)
        )
