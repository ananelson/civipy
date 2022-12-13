class CivipyException(Exception):
    pass


class CiviProgrammingError(CivipyException):
    pass


class NonUniqueSelectorException(CivipyException):
    pass


class CiviHTTPError(CivipyException):
    def __init__(self, r):
        self.r = r
        self.status_code = r.status_code
        self.message = r.text


class CiviAPIError(CivipyException):
    def __init__(self, data):
        self.code = data.get('error_code')
        self.message = data.get('error_message')
