# /api/app.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from graph_runner import run_graph

app = FastAPI()

# Allow frontend (Chainlit) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    user_id: str
    message: str

class MessageResponse(BaseModel):
    response: str

@app.post("/chat", response_model=MessageResponse)
async def chat_endpoint(req: MessageRequest):
    result = run_graph(user_id=req.user_id, message=req.message)
    return {"response": result.get("response", "")}
