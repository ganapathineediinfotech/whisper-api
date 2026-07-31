from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline


app = FastAPI()

translator = None


class TranslationRequest(BaseModel):
    text: str


def get_translator():

    global translator

    if translator is None:
        print("Loading Telugu to English model...")

        translator = pipeline(
            "translation",
            model="Helsinki-NLP/opus-mt-te-en"
        )

        print("Model loaded")

    return translator



@app.get("/")
def home():
    return {
        "status": "Telugu to English Translation API Running"
    }



@app.post("/translate")
def translate(request: TranslationRequest):

    model = get_translator()

    result = model(request.text)

    return {
        "telugu": request.text,
        "english": result[0]["translation_text"]
    }