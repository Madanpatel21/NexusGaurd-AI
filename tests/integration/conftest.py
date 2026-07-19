import os
import sys

import pytest
import requests

# Make the enterprise-sync `src` directory importable as the `src` package.
_ENT = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "cloud", "microservices", "enterprise-sync", "src",
)
sys.path.insert(0, _ENT)


def _reachable(url, timeout=1):
    try:
        requests.get(url, timeout=timeout)
        return True
    except requests.exceptions.RequestException:
        return False


@pytest.fixture
def stack():
    if not _reachable("http://localhost:8080/health"):
        pytest.skip("requires running docker-compose stack (cloud-api on :8080)")
    return True


@pytest.fixture
def fl_service():
    if not _reachable("http://localhost:8081/health"):
        pytest.skip("requires running federated-learning service on :8081")
    return True
