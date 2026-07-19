import subprocess


def test_service_restart(stack):
    # Simulate a pod restart and verify the service recovers.
    result = subprocess.run(
        ["kubectl", "rollout", "status", "deployment/nexusguard-api",
         "-n", "nexusguard", "--timeout=60s"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
