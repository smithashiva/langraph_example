# nodes/vector_db_node.py

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Dummy knowledge base (simulate chunks)
KNOWLEDGE_BASE = [
    {
        "topic": "retirement age",
        "content": "The standard retirement age in most countries is between 60 and 67, depending on the system."
    },
    {
        "topic": "401k",
        "content": "A 401(k) is a retirement savings plan sponsored by an employer. Contributions are tax-deferred."
    },
    {
        "topic": "pension plan",
        "content": "Pension plans provide a fixed monthly income after retirement, based on years of service and salary."
    },
    {
        "topic": "early retirement",
        "content": "Early retirement can be taken before 60, but may reduce pension benefits."
    }
]

def vector_db_node(state: Dict[str, Any]) -> Dict[str, Any]:
    user_input = state.get("user_input", "").lower()
    matched_chunks = []

    for doc in KNOWLEDGE_BASE:
        if doc["topic"] in user_input:
            matched_chunks.append(doc["content"])

    # Fallback: match by keywords if topic match failed
    if not matched_chunks:
        keywords = ["retire", "pension", "401", "age"]
        for doc in KNOWLEDGE_BASE:
            if any(keyword in user_input for keyword in keywords):
                matched_chunks.append(doc["content"])

    if matched_chunks:
        logger.info(f"[VectorDB] Retrieved {len(matched_chunks)} chunks")
    else:
        logger.info("[VectorDB] No relevant chunks found")

    # Add retrieved context to state
    state["retrieved_context"] = "\n".join(matched_chunks) or "No matching knowledge found."
    return state
