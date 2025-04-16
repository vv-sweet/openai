from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

HUNYUAN_API_KEY = os.environ.get("HUNYUAN_API_KEY")
HUNYUAN_URL = "https://api.hunyuan.cloud.tencent.com/v1/chat/completions"

class Message(BaseModel):
    role: str
    content: str

class OpenAIChatRequest(BaseModel):
    model: str
    messages: list[Message]

@app.post("/v1/chat/completions")
async def chat_completion(request: OpenAIChatRequest):
    headers = {
        "Authorization": f"Bearer {HUNYUAN_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": request.model,
        "messages": [m.dict() for m in request.messages],
        "enable_enhancement": True,
    }

    resp = requests.post(HUNYUAN_URL, json=payload, headers=headers)
    resp_json = resp.json()

    return {
        "id": "chatcmpl-fakeid",
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": resp_json["choices"][0]["message"]["content"]
            },
            "finish_reason": "stop"
        }],
        "usage": resp_json.get("usage", {})
    }