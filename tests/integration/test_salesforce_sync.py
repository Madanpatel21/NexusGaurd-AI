from unittest import mock

import requests


def test_case_creation():
    token_resp = mock.MagicMock()
    token_resp.json.return_value = {"access_token": "test-token"}
    case_resp = mock.MagicMock()
    case_resp.status_code = 201
    case_resp.json.return_value = {"id": "500xx0000001"}

    def fake_post(url, **kwargs):
        if "oauth2/token" in url:
            return token_resp
        return case_resp

    import salesforce_connector as sfc
    with mock.patch.object(requests, "post", side_effect=fake_post):
        connector = sfc.SalesforceConnector()
        case_id = connector.create_case(
            "edge-001", "High", {"vibration": 15.0, "temperature": 95.0}
        )
    assert case_id == "500xx0000001"
