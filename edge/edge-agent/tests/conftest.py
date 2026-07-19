import os
import sys
from unittest import mock

# Stub heavy/nonexistent native deps so the `src` package imports cleanly.
sys.modules.setdefault("tensorflow", mock.MagicMock())
sys.modules.setdefault("tensorflow.lite", mock.MagicMock())
sys.modules.setdefault("prometheus_client", mock.MagicMock())

# Make the sibling `src` package importable as `src.*` from tests.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
