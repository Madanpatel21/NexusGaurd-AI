#!/usr/bin/env python3
"""End-to-end voice test: speak a command -> Whisper -> JARVIS -> (optional) TTS.

Usage:
  python scripts/voice_test.py --command "Stop edge-001"
  python scripts/voice_test.py --audio stop_cmd.wav --device_id edge-001
  python scripts/voice_test.py --command "Simulate motor failure on edge-001" --speak
"""
import argparse
import os
import sys

import requests

VOICE_URL = os.getenv("VOICE_URL", "http://localhost:8082")
# When no audio file is provided, we synthesize one from --command via TTS,
# or (fallback) send the text straight to JARVIS by hitting the chat endpoint.
JARVIS_URL = os.getenv("JARVIS_URL", "http://localhost:8081")


def _post_json(url, payload, timeout=30):
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": str(e)}


def run_command(command, device_id=None, audio=None, speak=False):
    if audio and os.path.exists(audio):
        with open(audio, "rb") as f:
            resp = requests.post(
                f"{VOICE_URL}/api/v1/voice/command",
                files={"file": (os.path.basename(audio), f, "audio/wav")},
                data={"device_id": device_id},
                timeout=60,
            )
        print(f"[VOICE] {resp.status_code} {resp.text}")
        return

    # No audio: send text directly to JARVIS chat (same path Whisper would take).
    print(f"[CMD] {command}")
    result = _post_json(
        f"{JARVIS_URL}/api/v1/jarvis/chat",
        {"query": command, "device_id": device_id},
    )
    jarvis_response = result.get("response", result)
    print(f"[JARVIS] {jarvis_response}")

    if speak:
        tts = _post_json(
            f"{VOICE_URL}/api/v1/voice/speak", {"text": jarvis_response}
        )
        print(f"[TTS] {tts if 'error' in tts else 'audio returned'}")


def main():
    p = argparse.ArgumentParser(description="NexusGuard voice pipeline test")
    p.add_argument("--command", default="Stop edge-001", help="Voice command text")
    p.add_argument("--device_id", default="edge-001")
    p.add_argument("--audio", default=None, help="Path to a .wav recording")
    p.add_argument("--speak", action="store_true", help="Synthesize JARVIS reply")
    args = p.parse_args()

    run_command(args.command, args.device_id, args.audio, args.speak)


if __name__ == "__main__":
    sys.exit(main())
