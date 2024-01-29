from civipy.base.base import CiviCRMBase


def test_generate_search_query_using_string():
    search_query = CiviCRMBase._interface().search_query("id", {"id": "foo", "ignore": "bar"})
    assert search_query == {"id": "foo"}


def test_generate_search_query_using_list():
    search_query = CiviCRMBase._interface().search_query(
        ["id", "extra"], {"id": "foo", "extra": "baz", "ignore": "bar"}
    )
    assert search_query == {"id": "foo", "extra": "baz"}
