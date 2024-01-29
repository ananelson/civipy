from civipy import CiviContribution


def test_find_with_existing():
    contrib = CiviContribution.find_by_transaction_id(trxn_id="12345")

    assert isinstance(contrib, CiviContribution)
    assert contrib.display_name == "Sample Donor"
    assert contrib.trxn_id == "12345"
    assert contrib.civi["display_name"] == "Sample Donor"
    assert contrib.civi["trxn_id"] == "12345"

    # do some tests of setattr while we have an object
    #
    # existing civi attributes can be modified
    contrib.display_name = "New Name"
    assert contrib.civi["display_name"] == "New Name"
    assert "display_name" not in contrib.__dict__
    assert contrib.display_name == "New Name"

    # but other attributes won't affect civi dict
    contrib.foo = "bar"
    assert "foo" not in contrib.civi
    assert contrib.foo == "bar"

    # unless they are prefixed with civi_
    contrib.civi_foo = "bar"
    assert contrib.civi["foo"] == "bar"
    assert contrib.foo == "bar"
