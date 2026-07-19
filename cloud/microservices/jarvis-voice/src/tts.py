# cloud/microservices/jarvis-voice/src/tts.py
"""Local, privacy-focused Text-to-Speech using Coqui TTS."""
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TTS")

_model = None


def _load_model():
    from TTS.api import TTS as CoquiTTS
    # Lightweight English multi-speaker model; swap for a larger one if desired.
    return CoquiTTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")


def get_model():
    global _model
    if _model is None:
        _model = _load_model()
    return _model


def synthesize(text: str, output_path: str = "/tmp/jarvis_response.wav") -> str:
    """Synthesizes `text` to speech and returns the WAV file path."""
    try:
        get_model().tts_to_file(text=text, file_path=output_path)
        logger.info(f"TTS synthesized: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"TTS failed: {e}")
        return ""
