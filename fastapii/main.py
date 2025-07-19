# main.py
import chainlit as cl
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph_runner import run_graph  # your LangGraph runner logic

# --------------- FASTAPI SETUP ----------------

app = FastAPI()



class MessageRequest(BaseModel):
    user_id: str
    message: str

class MessageResponse(BaseModel):
    response: str

@app.post("/chat", response_model=MessageResponse)
async def chat_endpoint(req: MessageRequest):
    result = run_graph(user_id=req.user_id, message=req.message)
    return {"response": result.get("response", "---no response---")}


# --------------- CHAINLIT LOGIC ----------------

@cl.on_chat_start
async def start():
    await cl.Message(content="👋 Hello! Ask me anything about retirement planning.").send()

@cl.on_message
async def main(message: cl.Message):
    user_id = "demo-user"  # Replace with session/user logic if needed
    msg = message.content

    # Call FastAPI endpoint internally
    from httpx import AsyncClient
    async with AsyncClient() as client:
        resp = await client.post("http://localhost:8000/chat", json={"user_id": user_id, "message": msg})
        response_text = resp.json().get("response", "---no response---")

    await cl.Message(content=response_text).send()


# --------------- MOUNT FASTAPI ----------------

from chainlit.server import app as chainlit_app
chainlit_app.mount("/chat-api", app)  # Mount FastAPI at /chat-api
