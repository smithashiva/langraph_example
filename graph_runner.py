from flows.conversation_graph import build_conversation_graph
from state_schema import GraphState
from history_store import HistoryStore
import uuid


history_store = HistoryStore()
graph = build_conversation_graph()

def run_graph(user_id: str, message: str) -> dict:
    history = history_store.get_user_history(user_id)

    state = {
        "user_id": user_id,
        "input": message,
        "history": history + [{"role": "user", "content": message}]
    }

    final_state: GraphState = graph.invoke(state)

    history_store.append_user_message(user_id, "user", message)
    history_store.append_user_message(user_id, "assistant", final_state["response"])

    return final_state
