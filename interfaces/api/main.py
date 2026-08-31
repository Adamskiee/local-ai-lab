from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from fastapi.responses import JSONResponse

from core.rag.indexer import index_directory
from core.rag.retriever import retrieve, project_has_chunks
from core.config import OLLAMA_URL, OLLAMA_MODEL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    project_root: str

class IndexRequest(BaseModel):
    path: str

@app.get("/")
def root():
    return {"message": "Ollama FastAPI is running"}

@app.post("/index")
def index(request: IndexRequest):
    result = index_directory(request.path)
    return result

@app.post("/chat")
async def chat(request: ChatRequest):
    if not project_has_chunks(request.project_root):
        return {"response": "Project not indexed"}

    chunks = retrieve(request.message, request.project_root)
    if not chunks:
        return {"response": "I don't see that"}

    context = "\n".join(chunk["content"] for chunk in chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {request.message}"

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                },
            )
            response.raise_for_status()
            data = response.json()
            return {
                "response": data["response"],
                "sources": [
                    {"file_path": chunk["file_path"], "start_line": chunk["start_line"]}
                    for chunk in chunks
                ]
            }
    except (httpx.ConnectError, httpx.TimeoutException):
        raise HTTPException(status_code=503, detail="Ollama service is down or timed out")
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=502, detail="Ollama service returned an error")

