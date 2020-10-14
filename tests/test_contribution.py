from civipy import CiviContribution
from tests.utils import mocked_requests_get
from unittest.mock import patch


@patch('civipy.base.requests.get', side_effect=mocked_requests_get)
def test_find_with_existing(mock_http_get):

    contrib = CiviContribution.find_by_transaction_id(trxn_id="12345")

    assert isinstance(contrib, CiviContribution)
    assert contrib.display_name == "Sample Donor"
    assert contrib.trxn_id == "12345"
    assert contrib.civi['display_name'] == 'Sample Donor'
    assert contrib.civi['trxn_id'] == '12345'
    mock_http_get.assert_called_once()

    # do some tests of setattr while we have an object
    #
    # existing civi attributes can be modified
    contrib.display_name = "New Name"
    assert contrib.civi['display_name'] == 'New Name'
    assert not 'display_name' in contrib.__dict__
    assert contrib.display_name == "New Name"

    # but other attributes won't affect civi dict
    contrib.foo = 'bar'
    assert not 'foo' in contrib.civi
    assert contrib.foo == 'bar'

    # unless they are prefixed with civi_
    contrib.civi_foo = 'bar'
    assert contrib.civi['foo'] == 'bar'
    assert contrib.foo == 'bar'
