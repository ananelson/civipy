class CivipyException(Exception):
    pass


class NonUniqueEmailException(CivipyException):
    pass


class NonUniqueNameException(CivipyException):
    pass
