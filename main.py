import os
from flows.conversation_graph import build_conversation_graph
from dotenv import load_dotenv
load_dotenv()
print("✅ Loaded key:", os.getenv("OPENAI_API_KEY"))

# Build the graph
graph = build_conversation_graph()

# Initial state for the conversation
# state = {
#     "user_id": "user_123",
#     "history": ["Hi there!"]
#    }

# state = {
#     "user_id": "user_123",
#     "input": "Can you calculate my returns?",
#     "history": []
# }

state = {
    "user_id": "user_123",
    "input": "When should I retire?",
    "history": []
}

# Run the graph
output = graph.invoke(state)

# Show final state
print("\n--- Final State ---")
print(output)



#user - screen - input - gneral agent- calultion  -llm - router - calculation node - 