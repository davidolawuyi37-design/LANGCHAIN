from typing import TypedDict

class AssistantState(TypedDict):
    user_input: str
    route: str
    specialist_response: str
    final_response: str