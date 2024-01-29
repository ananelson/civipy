from civipy.base.config import SETTINGS
from civipy.exceptions import CiviProgrammingError
from civipy.interface.base import CiviValue, CiviResponse, BaseInterface as Interface
from civipy.interface.v3 import v3_interface
from civipy.interface.v4 import v4_interface


def get_interface():
    if SETTINGS.api_version == "4":
        return v4_interface
    if SETTINGS.api_version == "3":
        return v3_interface
    raise CiviProgrammingError(f"Invalid API version '{SETTINGS.api_version}' - cannot initialize interface.")


__all__ = ["get_interface", "CiviValue", "CiviResponse", "Interface"]
