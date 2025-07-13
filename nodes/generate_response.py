
from langgraph.graph import state

def generate_response_node(state):
    #last_input = state.get("input", "")
    last_input = state["history"][-1] if state["history"] else ""


    print(f"[GenerateResponse] Received input: {last_input}")
    response = "Hello, how can I help you?"
    return {"response": response}
