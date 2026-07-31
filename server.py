from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
import shutil
import os

app = FastAPI()

print("Loading Whisper Tiny...")

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

print("Loaded!")

@app.get("/")
def home():
    return {"status":"running"}

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):

    filename = f"uploads/{audio.filename}"

    with open(filename,"wb") as f:
        shutil.copyfileobj(audio.file,f)

    segments, info = model.transcribe(
        filename,
        language="te"
    )

    result=[]

    for s in segments:
        result.append({
            "start":s.start,
            "end":s.end,
            "text":s.text
        })

    os.remove(filename)

    return {
        "language":info.language,
        "segments":result
    }