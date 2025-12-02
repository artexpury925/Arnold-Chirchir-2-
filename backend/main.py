from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="Arnold Chirchir 2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VLLM_URL = "http://localhost:8001/v1"  # Worker runs here

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    messages = data["messages"]
    
    # Inject self-aware system prompt
    if not messages or messages[0]["role"] != "system":
        with open("../system_prompt.txt", "r") as f:
            system = f.read()
        messages.insert(0, {"role": "system", "content": system})

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{VLLM_URL}/chat/completions",
            json={
                "model": "arnold-chirchir-2",
                "messages": messages,
                "max_tokens": 4096,
                "temperature": 0.8
            },
            timeout=300
        )
        return resp.json()