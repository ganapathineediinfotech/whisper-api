from fastapi import FastAPI, UploadFile, File
import shutil
import whisper
import os

app = FastAPI()

print("Loading Whisper model...")

model = whisper.load_model("tiny")

print("Model Loaded")

@app.get("/")
def home():
    return {"status":"running"}

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):

    filepath = f"uploads/{audio.filename}"

    with open(filepath,"wb") as buffer:
        shutil.copyfileobj(audio.file,buffer)

    result = model.transcribe(
        filepath,
        language="te"
    )

    os.remove(filepath)

    return result