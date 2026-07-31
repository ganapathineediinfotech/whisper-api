from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
import shutil
import os

app = FastAPI()

print("Loading model...")

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

print("Model loaded")

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):

    filepath = f"uploads/{audio.filename}"

    with open(filepath, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    segments, info = model.transcribe(
        filepath,
        language="te"
    )

    result = {
        "language": info.language,
        "segments": []
    }

    for segment in segments:
        result["segments"].append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })

    os.remove(filepath)

    return result