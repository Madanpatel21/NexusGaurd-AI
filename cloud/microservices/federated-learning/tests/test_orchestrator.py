import unittest

from orchestrator import FederatedServer


class TestFederatedServer(unittest.TestCase):
    def test_init_model(self):
        server = FederatedServer()
        self.assertIsNotNone(server.global_model)
        self.assertEqual(len(server.clients), 0)

    def test_aggregate(self):
        server = FederatedServer()
        sd = server.global_model.state_dict()
        client_weights = [dict(sd), dict(sd)]
        result = server.aggregate(client_weights)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
