# cloud/microservices/jarvis-voice/src/voice_processor.py
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Voice-Processor")


def _load_model():
    """Lazily load the local Whisper model (privacy-focused, no cloud)."""
    import whisper
    return whisper.load_model("base")


# Module-level model handle (loaded on first use).
_model = None


def get_model():
    global _model
    if _model is None:
        _model = _load_model()
    return _model


def transcribe_audio(audio_file_path: str) -> str:
    """Converts an audio file to text using the local Whisper model."""
    try:
        result = get_model().transcribe(audio_file_path)
        text = result["text"].strip()
        logger.info(f"Transcribed: {text}")
        return text
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        return ""


def process_voice_command(command_text: str, device_id: str = None, jarvis_url: str = None):
    """Sends transcribed text to JARVIS Core for reasoning/action."""
    import requests

    if jarvis_url is None:
        jarvis_url = os.getenv("JARVIS_URL", "http://nexusguard-jarvis:8081")

    payload = {"query": command_text, "device_id": device_id}
    try:
        response = requests.post(f"{jarvis_url}/api/v1/jarvis/chat", json=payload, timeout=10)
        return response.json().get("response", "")
    except requests.RequestException as e:
        logger.error(f"JARVIS unreachable: {e}")
        return ""


if __name__ == "__main__":
    # Example: listen for a command
    audio_file = "input_command.wav"
    text = transcribe_audio(audio_file)
    if text:
        response = process_voice_command(text, "edge-001")
        print(f"JARVIS Response: {response}")
