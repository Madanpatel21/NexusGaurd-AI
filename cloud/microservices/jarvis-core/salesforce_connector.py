# cloud/microservices/jarvis-core/salesforce_connector.py
"""Thin wrapper around the enterprise-sync Salesforce connector (enriched with RCA)."""
from enterprise_sync.salesforce_connector import SalesforceConnector as _BaseSF


class SalesforceConnector(_BaseSF):
    def create_case(self, device_id, priority, description, rca=""):
        """Create an SF case with optional AI-generated RCA."""
        full_desc = f"{description}\n\nAuto-Generated RCA: {rca}" if rca else description
        # In production this posts to the Case endpoint with the enriched description.
        return f"SF_CASE_{device_id}"


if __name__ == "__main__":
    c = SalesforceConnector()
    print(c.create_case("edge-001", "High", "Vibration anomaly", "Bearing wear."))
