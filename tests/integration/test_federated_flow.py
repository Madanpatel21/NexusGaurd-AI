import requests


def test_model_aggregation(fl_service):
    weights = {"layer1": [0.1, 0.2], "layer2": [0.3, 0.4]}
    resp = requests.post("http://localhost:8081/update", json={"weights": weights})
    assert resp.status_code in (200, 201)

    model_resp = requests.get("http://localhost:8081/model")
    assert model_resp.status_code == 200
