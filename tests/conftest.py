import json
from pathlib import Path
import pytest
import civipy
import civipy.base.config


@pytest.fixture(autouse=True)
def mock_civi_rest_api(monkeypatch):
    civipy.init(
        rest_base="http://civipy/tests",
        user_key="xm1VJgt5grEYztkUHHjV995C",
        site_key="M5rohjMtEBaxDKDdXuk0U0QMGcdoYcV0",
        api_version="3",
        log_level="INFO",
    )
    monkeypatch.setattr("urllib3.request", mocked_request)


def mocked_request(*args, fields: dict[str, str], **kwargs):
    v = civipy.base.config.SETTINGS.api_version
    entity = fields["entity"]
    action = fields["action"]
    attr = next(filter(None, (fields.get(attr) for attr in ("contact_id", "email", "trxn_id"))), None)
    file = Path(__file__).with_name("responses") / f"{entity}_v{v}_{action}.json"
    if not file.is_file():
        raise Exception(f"Tests for v{v} {entity} action {action} not implemented")
    data = json.loads(file.read_text()).get(attr)
    if not data:
        raise Exception(f"Tests for {fields} not implemented")
    return MockResponse(data, 200)


class MockResponse:
    def __init__(self, json_data, status):
        self.json_data = json_data
        self.status = status
        self.url = "http://civipy/tests"

    def json(self):
        return self.json_data
