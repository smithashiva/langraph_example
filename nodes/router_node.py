def router_node(state):
    user_input = state.get("input", "").lower()
    print(f"[RouterNode] Routing input: {user_input}")



    if "calculate" in user_input or "add" in user_input:
        return "calculation"
    else:
        return "advise"