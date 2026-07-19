# cloud/microservices/enterprise-sync/src/salesforce_connector.py
import os
import requests


class SalesforceConnector:
    def __init__(self):
        self.token = self.get_access_token()
        self.base_url = os.getenv("SF_BASE_URL")

    def get_access_token(self):
        # OAuth2 Client Credentials Flow
        auth = {
            "grant_type": "client_credentials",
            "client_id": os.getenv("SF_CLIENT_ID"),
            "client_secret": os.getenv("SF_CLIENT_SECRET"),
        }
        resp = requests.post(f"{os.getenv('SF_AUTH_URL')}/services/oauth2/token", data=auth)
        return resp.json()["access_token"]

    def create_case(self, device_id, priority, data, rca=""):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        description = f"Vibration: {data['vibration']}, Temp: {data['temperature']}"
        if rca:
            description += f"\n\nAuto-Generated RCA: {rca}"
        payload = {
            "Subject": f"Critical Anomaly: {device_id}",
            "Description": description,
            "Priority": priority,
            "Type": "Equipment Failure",
        }
        resp = requests.post(
            f"{self.base_url}/services/data/v58.0/sobjects/Case/",
            headers=headers,
            json=payload,
        )
        if resp.status_code == 201:
            return resp.json()["id"]
        raise Exception(f"SF Error: {resp.text}")
