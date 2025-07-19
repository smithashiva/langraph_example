import traceback
from flows.conversation_graph import build_conversation_graph
from flows.state_schema import GraphState
from history_store import HistoryStore
import uuid


history_store = HistoryStore()
graph = build_conversation_graph()

print("✅ graph_runner.py LOADED (LATEST VERSION)")

def run_graph(user_id: str, message: str) -> dict:
    history = []
    try:
        history = history_store.get_user_history(user_id)
        print(f"[History Debug] Retrieved history for {user_id}: {history}")  
        if not history:
            print(f"[History Debug] No history found for {user_id}, starting fresh.")

        state = {
            "user_id": user_id,
            "input": message,
            "history": history + [{"role": "user", "content": message}]
        }

        print(f"📤 [DEBUG] Invoking graph with state: {state}")
        final_state: GraphState = graph.invoke(state)    
        print(f"[run_graph] Final state: {final_state}")


        # Try to append user message
        if not history_store.append_user_message(user_id, "user", message):
            history_store.insert_new_session(user_id, state)
            history_store.append_user_message(user_id, "user", message)

        # Try to append assistant response
        if not history_store.append_user_message(user_id, "assistant", final_state["response"]):
            history_store.insert_new_session(user_id, state)
            history_store.append_user_message(user_id, "assistant", final_state["response"])


        return final_state
    except Exception as e:
            print(f"[run_graph] Error: {e}")
            print("🚨 Inside EXCEPTION handler — printing fallback message now!")
            traceback.print_exc()
            return {
                "user_id": user_id,
                "input": message,
                "response": "Sorry, I'm having trouble fetching advice right now. ---V3---",
                "messages": history + [{"role": "user", "content": message}]
            }