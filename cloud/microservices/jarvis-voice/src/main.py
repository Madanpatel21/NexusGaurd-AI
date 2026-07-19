# cloud/microservices/jarvis-voice/src/main.py
import os

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from voice_processor import transcribe_audio, process_voice_command
from tts import synthesize

app = FastAPI(title="NexusGuard Voice Interface", version="1.0.0")


@app.post("/api/v1/voice/command")
async def voice_command(file: UploadFile = File(...), device_id: str = None):
    # Save uploaded audio temporarily
    audio_path = f"/tmp/{file.filename}"
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    try:
        text = transcribe_audio(audio_path)
        response = process_voice_command(text, device_id)
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

    return {"transcription": text, "jarvis_response": response}


@app.post("/api/v1/voice/speak")
async def speak(body: dict):
    """Synthesize JARVIS text into speech (local TTS) and return the WAV."""
    text = body.get("text", "")
    if not text:
        return {"error": "missing 'text'"}, 400
    wav_path = synthesize(text)
    if not wav_path or not os.path.exists(wav_path):
        return {"error": "TTS synthesis failed"}, 500
    return FileResponse(wav_path, media_type="audio/wav", filename="jarvis_response.wav")


@app.post("/api/v1/voice/command-and-speak")
async def command_and_speak(file: UploadFile = File(...), device_id: str = None):
    """Full pipeline: transcribe -> JARVIS -> speak the response back."""
    audio_path = f"/tmp/{file.filename}"
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    try:
        text = transcribe_audio(audio_path)
        response = process_voice_command(text, device_id)
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

    wav_path = synthesize(response)
    if wav_path and os.path.exists(wav_path):
        return FileResponse(
            wav_path, media_type="audio/wav", filename="jarvis_response.wav"
        )
    return {"transcription": text, "jarvis_response": response}


@app.get("/health")
async def health():
    return {"status": "Voice Interface Online"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8082)
