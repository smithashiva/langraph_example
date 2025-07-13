from langgraph.graph import StateGraph
from flows.state_schema import GraphState

from nodes.init_session import init_session_node
from nodes.generate_response import generate_response_node
from nodes.store_session import store_session_node
from nodes.fallback import fallback_node
from nodes.router_node import router_node
from nodes.calculation_node import calculation_node
from nodes.advise_node import advise_node
from nodes.vector_db_node import vector_db_node

def build_conversation_graph():
    builder = StateGraph(GraphState)

    builder.add_node("init", init_session_node)
    builder.add_node("respond", generate_response_node)
    builder.add_node("router", router_node)
    builder.add_node("calculation", calculation_node)
    builder.add_node("advise", advise_node)
    builder.add_node("store", store_session_node)
    builder.add_node("fallback", fallback_node)
    builder.add_node("vector_db", vector_db_node) 


    builder.set_entry_point("init")
    #builder.add_edge("init", "router")
    builder.add_conditional_edges("init", router_node, {
        "calculation": "calculation",
       # "advise": "advise"
        "advise": "vector_db"  # ✅ 

    })
    builder.add_edge("calculation", "store")
   # builder.add_edge("advise", "store")
    builder.add_edge("vector_db", "advise")  # ✅ vector DB to advise
    builder.add_edge("advise", "store")

    # Optional fallback
    #builder.set_error_handler("fallback")- only in new version

    return builder.compile()
