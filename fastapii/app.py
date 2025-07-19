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

    # Debugging outputs
    print("🔁 [DEBUG] Full result from run_graph:", result)
    print("🔁 [DEBUG] Extracted response:", result.get("response"))

    # Fallback if response key is missing or empty
    return {
        "response": result.get("response", "---NO RESPONSE RETURNED FROM GRAPH---")
    }