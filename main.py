from fastapi import FastAPI
from pydantic import BaseModel
from googletrans import Translator

app = FastAPI()
translator = Translator()

class TranslationRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "Telugu to English Translation API Running"}

@app.post("/translate")
def translate(request: TranslationRequest):
    # Google Translate auto-detects source language
    result = translator.translate(request.text, dest='en')
    return {
        "telugu": request.text,
        "english": result.text
    }