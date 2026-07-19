# Salesforce Integration

REST/SOAP bridge for service case creation and customer alert sync.

## Files
- `../src/salesforce_connector.py` — `SalesforceConnector` using OAuth2 client credentials.
- `../src/sync_service.py` — orchestrates unified SAP + Salesforce sync.

## Configuration (via Vault)
- `SF_CLIENT_ID`, `SF_CLIENT_SECRET`, `SF_AUTH_URL`, `SF_BASE_URL`
- API: `/services/data/v58.0/sobjects/Case/`
