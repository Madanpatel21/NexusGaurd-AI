import requests

class FederatedClient:
    def __init__(self, server_url):
        self.server_url = server_url

    def send_weights(self, weights):
        requests.post(f"{self.server_url}/update", json={"weights": weights})

    def receive_model(self):
        resp = requests.get(f"{self.server_url}/model")
        return resp.json()
