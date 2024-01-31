from civipy import CiviContact


def test_get_with_existing():
    contact_info = CiviContact.action("get", email="validunique@example.com")

    assert isinstance(contact_info, dict)
    assert contact_info["count"] == 1
    assert len(contact_info["values"]) == 1


def test_get_no_match():
    contact_info = CiviContact.action("get", email="unknown@example.com")

    assert isinstance(contact_info, dict)
    assert contact_info["count"] == 0
    assert len(contact_info["values"]) == 0


def test_find_with_existing():
    contact = CiviContact.find(email="validunique@example.com")

    assert isinstance(contact, CiviContact)
    assert contact.display_name == "Valid Unique"
    assert contact.email == "validunique@example.com"
    assert contact.civi["display_name"] == "Valid Unique"
    assert contact.civi["email"] == "validunique@example.com"

    # do some tests of setattr while we have an object
    #
    # existing civi attributes can be modified
    contact.display_name = "New Name"
    assert contact.civi["display_name"] == "New Name"
    assert "display_name" not in contact.__dict__
    assert contact.display_name == "New Name"

    # but other attributes won't affect civi dict
    contact.foo = "bar"
    assert "foo" not in contact.civi
    assert contact.foo == "bar"

    # unless they are prefixed with civi_
    contact.civi_foo = "bar"
    assert contact.civi["foo"] == "bar"
    assert contact.foo == "bar"


def test_find_and_update_with_existing():
    contact = CiviContact.find_and_update(where={"email": "validunique@example.com"}, display_name="Updated Name")

    assert isinstance(contact, CiviContact)
    assert contact.display_name == "Updated Name"
    assert contact.email == "validunique@example.com"
    assert contact.civi["display_name"] == "Updated Name"
    assert contact.civi["email"] == "validunique@example.com"


def test_find_no_match():
    contact = CiviContact.find(email="unknown@example.com")

    assert contact is None


def test_find_all_no_match():
    contact = CiviContact.find_all(email="unknown@example.com")

    assert contact == []


def test_find_or_create_with_existing():
    contact = CiviContact.find_or_create(where={"email": "validunique@example.com"})

    assert isinstance(contact, CiviContact)
    assert contact.display_name == "Valid Unique"
    assert contact.email == "validunique@example.com"
    assert contact.civi["display_name"] == "Valid Unique"
    assert contact.civi["email"] == "validunique@example.com"
