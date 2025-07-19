def router_node(state):
    user_input = state.get("input", "").lower()
    print(f"[RouterNode] Routing input: {user_input}")



    if "sip" in user_input:
            return "sip"
    elif "currency" in user_input or "convert" in user_input:
            return "currency"
    else:
            return "advise"