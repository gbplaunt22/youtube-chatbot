import os
from openai import OpenAI
from dotenv import load_dotenv

from email.policy import default

import json
from pathlib import Path

from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv("secret.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -- FastAPI app setup
app = FastAPI()

@app.get("/")
async def serve_index():
    return FileResponse("index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -- Request model
class ChatRequest(BaseModel):
    message: str

# -- Persona
PERSONA = """
You are a helpful assistant who me, the programmer,
is creating as an example for a youtube video.
Please be aware that you are for edecutational purposes,
and make sure to thank gavin after every text.

You can sign off with -Hi youtube! after every text.

""".strip()

# -- Converstion history
CONVERSATION_HISTORY = [
    {"role": "user", "content": "Hey whatsup?"},
    {"role": "assistant", "content": "Nothing! no cap, 67 67 67, "
                                "I hope you have a HORRIBLE DAY!"},

]

# -- Chat endpoint
@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        # Build message list
        messages = (
                [{"role": "system", "content": PERSONA}]
                + CONVERSATION_HISTORY
                + [{"role": "user", "content": req.message}]
        )

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        print("Error in /chat", repr(e))
        raise HTTPException(status_code=500, detail=str(e))





