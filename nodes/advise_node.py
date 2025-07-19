import os
from openai import OpenAI

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = OpenAI(
    api_key="gsk_UW65qTaQyIhjSm5eahB2WGdyb3FY0SHjpTj1vkJcSUT8AaskHdv",
    base_url="https://api.groq.com/openai/v1"  # or Together/OpenRouter etc.
)

def advise_node(state):
    user_id = state.get("user_id", "guest_user")
    messages = state.get("messages", [])
    vector_context = state.get("vector_context", "")

    latest_question = messages[-1]["content"] if messages else "What can you advise me on?"

    system_prompt = f"""
    You are a helpful and honest retirement financial advisor.
    Use the following retrieved context and prior session messages to respond intelligently.

    Context: {vector_context}
    """

    openai_messages = [
        {"role": "system", "content": system_prompt},
        *messages,
        {"role": "user", "content": latest_question}
    ]

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192", #model="gpt-3.5-turbo",
            messages=openai_messages
        )
        #print(f"[AdviseNode] OpenAI response: {response}")
       
        reply = response.choices[0].message.content.strip()
        return {
            "user_id": user_id,
            "messages": messages + [{"role": "assistant", "content": reply}],
            "response": reply
        }
    except Exception as e:
        print(f"[AdviseNode] OpenAI Error: {e}")
        return {
            "user_id": user_id,
            "messages": messages,
            "response": "Sorry, I'm having trouble fetching advice right now."
        }

