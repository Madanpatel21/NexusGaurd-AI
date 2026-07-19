import sys
from unittest import mock

import pytest


@pytest.fixture
def patch_external(monkeypatch):
    # Stub heavy/nonexistent deps so the module imports cleanly.
    tensorflow = mock.MagicMock()
    monkeypatch.setitem(sys.modules, "tensorflow", tensorflow)
    tflite = mock.MagicMock()
    monkeypatch.setitem(sys.modules, "tensorflow.lite", tflite)
    prometheus = mock.MagicMock()
    monkeypatch.setitem(sys.modules, "prometheus_client", prometheus)
    with mock.patch.dict("os.environ", {"DEVICE_ID": "edge-test", "CLOUD_URL": "http://cloud:8080"}):
        yield


def test_agent_init_defaults(patch_external):
    from src.agent import EdgeAgent
    agent = EdgeAgent()
    assert agent.device_id == "edge-test"
    assert agent.cloud_url == "http://cloud:8080"


def test_agent_simulate_sensor_data_shape(patch_external):
    from src.agent import EdgeAgent
    agent = EdgeAgent()
    data = agent.simulate_sensor_data()
    assert set(["vibration", "temperature"]).issubset(data.keys())


def test_agent_run_loop_iteration(patch_external):
    from src.agent import EdgeAgent
    agent = EdgeAgent()

    with mock.patch.object(agent, "send_to_cloud") as send_mock, \
         mock.patch.object(agent, "infer", return_value=False), \
         mock.patch("src.agent.time.sleep"):
        # Run a single iteration of the loop body.
        data = agent.simulate_sensor_data()
        if agent.infer(data):
            agent.actuate()
        agent.send_to_cloud(data)
        send_mock.assert_called_once()
