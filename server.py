from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
import shutil
import os

app = FastAPI()

print("Loading model...")
model = WhisperModel("tiny", device="cpu", compute_type="int8")
print("Model loaded")

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):

    print("Upload started")

    filepath = f"uploads/{audio.filename}"

    with open(filepath, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    print("File saved:", filepath)

    print("Starting transcription...")

    segments, info = model.transcribe(
        filepath,
        language="te"
    )

    print("Transcription finished")

    result = []

    for s in segments:
        result.append({
            "start": s.start,
            "end": s.end,
            "text": s.text
        })

    os.remove(filepath)

    print("Sending response")

    return {
        "language": info.language,
        "segments": result
    }