def store_session_node(state):
    messages = state.get("messages", [])
    response = state.get("response", "")  
    messages.append({"from": "bot", "message": response})
    print(f"[StoreSession] Messages so far: {messages}")
    return {"messages": messages}
