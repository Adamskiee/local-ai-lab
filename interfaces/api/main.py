from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"message": "Ollama FastAPI is running"}


@app.post("/chat")
def chat(request: ChatRequest):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:3b",
            "prompt": request.message,
            "stream": False,
        },
    )

    response.raise_for_status()

    data = response.json()

    return {
        "response": data["response"]
    }
