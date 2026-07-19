from unittest import mock


def test_network_delay():
    # Validates the Chaos Mesh NetworkChaos manifest is well-formed.
    import yaml
    with open("tests/chaos/chaos-mesh-config.yaml") as f:
        docs = list(yaml.safe_load_all(f))
    network_chaos = [d for d in docs if d and d.get("kind") == "NetworkChaos"]
    assert len(network_chaos) >= 1
    assert network_chaos[0]["spec"]["action"] == "delay"
