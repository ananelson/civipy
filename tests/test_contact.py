from civipy import CiviContact
from tests.utils import mocked_requests_get
from tests.utils import mocked_requests_post
from unittest.mock import patch


@patch("civipy.base.requests.get", side_effect=mocked_requests_get)
def test_get_with_existing(mock_http_get):
    contact_info = CiviContact._get(email="validunique@example.com")

    assert isinstance(contact_info, dict)
    assert contact_info["count"] == 1
    assert len(contact_info["values"]) == 1
    mock_http_get.assert_called_once()


@patch("civipy.base.requests.get", side_effect=mocked_requests_get)
def test_get_no_match(mock_http_get):
    contact_info = CiviContact._get(email="unknown@example.com")

    assert isinstance(contact_info, dict)
    assert contact_info["count"] == 0
    assert len(contact_info["values"]) == 0
    mock_http_get.assert_called_once()


@patch("civipy.base.requests.get", side_effect=mocked_requests_get)
def test_find_with_existing(mock_http_get):
    contact = CiviContact.find(search_key_name="email", email="validunique@example.com")

    assert isinstance(contact, CiviContact)
    assert contact.display_name == "Valid Unique"
    assert contact.email == "validunique@example.com"
    assert contact.civi["display_name"] == "Valid Unique"
    assert contact.civi["email"] == "validunique@example.com"
    mock_http_get.assert_called_once()

    # do some tests of setattr while we have an object
    #
    # existing civi attributes can be modified
    contact.display_name = "New Name"
    assert contact.civi["display_name"] == "New Name"
    assert not "display_name" in contact.__dict__
    assert contact.display_name == "New Name"

    # but other attributes won't affect civi dict
    contact.foo = "bar"
    assert not "foo" in contact.civi
    assert contact.foo == "bar"

    # unless they are prefixed with civi_
    contact.civi_foo = "bar"
    assert contact.civi["foo"] == "bar"
    assert contact.foo == "bar"


@patch("civipy.base.requests.get", side_effect=mocked_requests_get)
@patch("civipy.base.requests.post", side_effect=mocked_requests_post)
def test_find_and_update_with_existing(mock_http_get, mock_http_post):
    contact = CiviContact.find_and_update(
        search_key_name="email", email="validunique@example.com", display_name="Updated Name"
    )

    assert isinstance(contact, CiviContact)
    assert contact.display_name == "Updated Name"
    assert contact.email == "validunique@example.com"
    assert contact.civi["display_name"] == "Updated Name"
    assert contact.civi["email"] == "validunique@example.com"
    mock_http_get.assert_called_once()
    mock_http_post.assert_called_once()


@patch("civipy.base.requests.get", side_effect=mocked_requests_get)
def test_find_no_match(mock_http_get):
    contact = CiviContact.find(search_key_name="email", email="unknown@example.com")

    assert contact is None
    mock_http_get.assert_called_once()


@patch("civipy.base.requests.get", side_effect=mocked_requests_get)
def test_find_all_no_match(mock_http_get):
    contact = CiviContact.find_all(search_key_name="email", email="unknown@example.com")

    assert contact == []
    mock_http_get.assert_called_once()


@patch("civipy.base.requests.get", side_effect=mocked_requests_get)
def test_find_or_create_with_existing(mock_http_get):
    contact = CiviContact.find_or_create(search_key_name="email", email="validunique@example.com")

    assert isinstance(contact, CiviContact)
    assert contact.display_name == "Valid Unique"
    assert contact.email == "validunique@example.com"
    assert contact.civi["display_name"] == "Valid Unique"
    assert contact.civi["email"] == "validunique@example.com"
    mock_http_get.assert_called_once()
