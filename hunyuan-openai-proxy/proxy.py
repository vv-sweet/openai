from fastapi import FastAPI
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    api_key=os.environ.get("HUNYUAN_API_KEY"),
    base_url="https://api.hunyuan.cloud.tencent.com/v1"
)

@app.post("/v1/chat/completions")
async def chat(request: dict):
    messages = request.get("messages", [])
    model = request.get("model", "hunyuan-turbos-latest")

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response
