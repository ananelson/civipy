from civipy.base import CiviCRMBase

# Most CiviCRMBase features tested in test_contact.py

def test_generate_search_query_using_string():
    search_query = CiviCRMBase._search_query('id', {'id' : 'foo', 'ignore' : 'bar'})
    assert search_query == {'id' : 'foo'}

def test_generate_search_query_using_list():
    search_query = CiviCRMBase._search_query(['id', 'extra'], {'id' : 'foo', 'extra' : 'baz', 'ignore' : 'bar'})
    assert search_query == {'id' : 'foo', 'extra' : 'baz'}

def test_provided_entity_name_left_alone():
    assert CiviCRMBase._entity("Contact") == "Contact"
