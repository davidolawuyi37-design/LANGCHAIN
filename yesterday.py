from langgraph.graph import StateGraph, START, END
from typing import TypedDict

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import SecretStr
import os

class HealthState(TypedDict):
    health_topic: str
    explanation: str

load_dotenv()

llm = ChatOpenAI(
    api_key=SecretStr(os.environ["DEEPSEEK_API_KEY"]),
    base_url="https://api.deepseek.com",
    model="deepseek-chat"
)

def explain_health_topic(state: HealthState):
    health_topic = state["health_topic"]

    response = llm.invoke(
        f"Explain this health topic '{health_topic}' in detail, including its causes, symptoms, mode of transmission, identification of infected persons and potential treatments."
    )

    return {
        "explanation": response.content
    }

def additional_info(state: HealthState):
    explanation = state["explanation"]

    additional_response = llm.invoke(
        f"Provide additional information on the health topic based on the following explanation: {explanation}"
    )

    return {
        "explanation": additional_response.content
    }

def clean_explanation(state: HealthState):
    explanation = state["explanation"]

    cleaned = explanation.replace("*", "")

    return {
        "explanation": cleaned
    }

builder = StateGraph(HealthState)

builder.add_node("explain_health_topic", explain_health_topic)
builder.add_node("additional_info", additional_info)
builder.add_node("clean_explanation", clean_explanation)

builder.add_edge(START, "explain_health_topic")
builder.add_edge("explain_health_topic", "additional_info")
builder.add_edge("additional_info", "clean_explanation")
builder.add_edge("clean_explanation", END)

graph = builder.compile()

health_topic = input("Enter a health topic to explain: ")
result = graph.invoke(HealthState(health_topic=health_topic, explanation=""))

print("\nEXPLANATION:")
print(result["explanation"])