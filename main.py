from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
 
app = FastAPI()



translator = None


def get_translator():
    global translator

    if translator is None:
        translator = pipeline(
            "translation",
            model="Helsinki-NLP/opus-mt-en-te"
        )

    return translator


class TranslationRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "status": "English Telugu Translation API Running"
    }

@app.post("/translate")
def translate(request: TranslationRequest):

    model = get_translator()

    result = model(request.text)

    return {
        "english": request.text,
        "telugu": result[0]["translation_text"]
    }