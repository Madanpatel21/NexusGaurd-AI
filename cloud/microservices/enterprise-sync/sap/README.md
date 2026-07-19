# SAP Integration

RFC/IDoc bridge for maintenance ticket and asset synchronization.

## Files
- `../src/sap_connector.py` — `SAPConnector` using `pyrfc`.
- `../src/sync_service.py` — orchestrates unified SAP + Salesforce sync.

## Configuration (via Vault)
- `SAP_USER`, `SAP_PASS`, `SAP_HOST`, `SAP_SYSNR`, `SAP_CLIENT`
- Target FM: `Z_CREATE_MAINTENANCE_TICKET` / `Z_CREATE_TICKET`
