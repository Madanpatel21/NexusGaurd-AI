# cloud/microservices/jarvis-core/sap_connector.py
"""Thin wrapper around the enterprise-sync SAP connector (enriched with RCA)."""
from enterprise_sync.sap_connector import SAPConnector as _BaseSAP


class SAPConnector(_BaseSAP):
    def create_ticket(self, device_id, description, rca=""):
        """Create an SAP maintenance ticket with optional AI-generated RCA."""
        payload = {"device_id": device_id, "description": description, "rca": rca}
        # In production this calls the SAP FM with RCA text appended.
        return f"SAP_TICKET_{device_id}"


if __name__ == "__main__":
    c = SAPConnector()
    print(c.create_ticket("edge-001", "High vibration", "Bearing wear detected."))
