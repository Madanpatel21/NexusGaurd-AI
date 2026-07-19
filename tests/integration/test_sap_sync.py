from unittest import mock

import sys


def test_ticket_creation():
    # Mock the ERP SDK so the integration test runs without live SAP.
    sap = mock.MagicMock()
    sap_connection = mock.MagicMock()
    sap_connection.call.return_value = {"NOTIFICATION_ID": "000100"}
    sap.Connection.return_value = sap_connection
    with mock.patch.dict(sys.modules, {"pyrfc": sap}):
        import sap_connector as sc
        connector = sc.SAPConnector()
        ticket = connector.create_ticket("edge-001", {"vibration": 15.0, "temperature": 95.0})
    assert ticket == {"NOTIFICATION_ID": "000100"}
