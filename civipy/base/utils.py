from typing import TYPE_CHECKING
from civipy.exceptions import NoResultError, NonUniqueResultError, CiviProgrammingError

if TYPE_CHECKING:
    from civipy.interface import CiviValue, CiviResponse


def get_unique(response: "CiviResponse") -> "CiviValue":
    """Enforce that exactly one record was returned in `response` and return just the record."""
    if isinstance(response["values"], dict):
        ident = list(response["values"].keys())[0]
        return get_unique_value_for_id(ident, response)
    else:
        return get_unique_value(response)


def get_unique_value(response: "CiviResponse") -> "CiviValue":
    """Return one value from a non-indexed response."""
    assert_unique(response)
    return response["values"][0]


def get_unique_value_for_id(record_id: str, response: "CiviResponse") -> "CiviValue":
    """Return one value from an indexed response."""
    assert_unique(response)
    return response["values"][record_id]


def assert_unique(response: "CiviResponse") -> None:
    """Raise exception if `response` does not have exactly one record."""
    if not response or "count" not in response:
        raise CiviProgrammingError(f"Unexpected response {response}")
    count = response["count"]
    if count == 0:
        raise NoResultError("No results in response.")
    if count > 1:
        raise NonUniqueResultError(f"Response is not unique, has {count} results.")
