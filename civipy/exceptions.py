from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from urllib3 import BaseHTTPResponse


class CivipyException(Exception):
    pass


class CiviProgrammingError(CivipyException):
    pass


class NonUniqueSelectorException(CivipyException):
    pass


class CiviHTTPError(CivipyException):
    def __init__(self, r: "BaseHTTPResponse"):
        self.r = r
        self.status_code = r.status
        self.message = r.data.decode("utf-8", errors="replace")


class CiviAPIError(CivipyException):
    def __init__(self, data):
        self.code = data.get("error_code")
        self.message = data.get("error_message")
