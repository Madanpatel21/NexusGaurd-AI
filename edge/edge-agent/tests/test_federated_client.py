from unittest import mock

import pytest


@pytest.fixture
def client(monkeypatch):
    import src.federated_client as fc
    return fc.FederatedClient("http://fl:8080")


def test_send_weights_posts(client, monkeypatch):
    import src.federated_client as fc
    post = mock.MagicMock()
    monkeypatch.setattr(fc.requests, "post", post)
    client.send_weights({"w": [1, 2, 3]})
    post.assert_called_once()
    args, kwargs = post.call_args
    assert args[0].endswith("/update")
    assert kwargs["json"] == {"weights": {"w": [1, 2, 3]}}


def test_receive_model_gets(client, monkeypatch):
    import src.federated_client as fc
    resp = mock.MagicMock()
    resp.json.return_value = {"global_model": "v2"}
    get = mock.MagicMock(return_value=resp)
    monkeypatch.setattr(fc.requests, "get", get)
    assert client.receive_model() == {"global_model": "v2"}
