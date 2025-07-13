from typing import TypedDict, List

class GraphState(TypedDict):
    user_id: str
    input: str
    history: List[str]
    response: str
