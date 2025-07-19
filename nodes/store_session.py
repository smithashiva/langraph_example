import uuid
from datetime import datetime
from history_store import HistoryStore

history_store = HistoryStore()

def store_session_node(state):
    user_id = state["user_id"]
    response = state.get("response", "")

    # Prepare history item
    new_message = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,  # optional — not required, but safe to include
        "role": "assistant",
        "content": response,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Append to history in state
    history = state.get("history", [])
    history.append(new_message)
    state["history"] = history

    # Persist updated state to DB
    session_state = {
        "input": state.get("input", ""),
        "history": history,
        "response": response
    }
    history_store.update_session_state(user_id, session_state)

    print(f"[StoreSession] Stored {len(history)} messages for user {user_id}")
    return state



def store_session_node_old(state):
    messages = state.get("messages", [])
    response = state.get("response", "")  
    messages.append({"from": "bot", "message": response})
    print(f"[StoreSession] Messages so far: {messages}")
    return {"messages": messages}


