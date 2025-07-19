import requests

url = "http://localhost:8000/chat"

payload = {
    "user_id": "88fe35d1-75a4-4675-a3d2-d9c119a0e4c2",
    "message": "hello how are you ?",
   # "message": "What are some good investment strategies for someone in their 30s?"
   # "message": "What about retirement planning?"
}

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    print("🧠 LLM Response:\n", data["response"])
except requests.exceptions.RequestException as e:
    print("❌ Request failed:", e)
