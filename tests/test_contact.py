from civipy import CiviContact
from unittest.mock import patch
from tests.utils import mocked_requests_get

@patch('civipy.base.requests.get', side_effect=mocked_requests_get)
def test_get(mock_http_get):
    contact = CiviContact._get(email="validunique@example.com")
    assert contact['count'] == 1
    assert len(contact['values']) == 1

@patch('civipy.base.requests.get', side_effect=mocked_requests_get)
def test_find(mock_http_get):
    contact = CiviContact.find(search_key_name = 'email', email = "validunique@example.com")
    assert isinstance(contact, CiviContact)
    assert contact.civi['display_name'] == 'Valid Unique'
    assert contact.civi['email'] == 'validunique@example.com'
