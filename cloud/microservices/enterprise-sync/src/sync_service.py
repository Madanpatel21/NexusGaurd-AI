import requests

from sap_connector import SAPConnector
from salesforce_connector import SalesforceConnector


class EnterpriseSyncService:
    def __init__(self, jarvis_url=None):
        self.sap = SAPConnector()
        self.sf = SalesforceConnector()
        self.jarvis_url = jarvis_url or "http://nexusguard-jarvis:8081"

    def _ask_jarvis_rca(self, device_id, anomaly_data):
        """Ask JARVIS for Root Cause Analysis on an anomaly."""
        try:
            resp = requests.post(
                f"{self.jarvis_url}/api/v1/jarvis/chat",
                json={
                    "query": f"Root cause analysis for high vibration on {device_id}.",
                    "device_id": device_id,
                },
                timeout=5,
            )
            return resp.json().get("response", "")
        except requests.RequestException as e:
            print(f"JARVIS RCA lookup failed: {e}")
            return ""

    def handle_anomaly(self, device_id, anomaly_data):
        # 1. Ask JARVIS for Root Cause Analysis
        rca_text = self._ask_jarvis_rca(device_id, anomaly_data)

        # 2. Create SAP Maintenance Ticket (enriched with RCA)
        sap_ticket_id = self.sap.create_ticket(
            device_id, anomaly_data, rca=rca_text
        )

        # 3. Create Salesforce Case (enriched with RCA)
        sf_case_id = self.sf.create_case(
            device_id, "High", anomaly_data, rca=rca_text
        )

        # 4. Update Internal DB
        db.create_sync_record(device_id, sap_ticket_id, sf_case_id)

        return {"sap": sap_ticket_id, "sf": sf_case_id, "rca": rca_text}
