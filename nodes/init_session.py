def init_session_node(state):
    user_id = state.get("user_id", "guest_user")
    print(f"[InitSession] Starting session for: {user_id}")
    return {"user_id": user_id, "messages": []}
