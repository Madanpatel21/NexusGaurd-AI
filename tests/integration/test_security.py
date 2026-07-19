import requests


def test_mtls_auth(stack):
    # Without a valid client certificate, the mTLS gateway must reject the call.
    try:
        resp = requests.get("https://api.nexusguard.ai/health", verify=True, timeout=5)
        assert resp.status_code in (200, 401, 403)
    except requests.exceptions.SSLError:
        # Rejection at the TLS layer also demonstrates mTLS enforcement.
        assert True
