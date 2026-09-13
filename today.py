from langgraph.graph import StateGraph, START, END
from typing import TypedDict

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import SecretStr
import os

load_dotenv()

class TechState(TypedDict):
    topic: str
    explanation: str

llm = ChatOpenAI(
    api_key=SecretStr(os.environ["DEEPSEEK_API_KEY"]),
    base_url="https://api.deepseek.com",
    model="deepseek-chat"
)

def explain_tech(state: TechState):
    topic = state["topic"]

    response = llm.invoke(
        f"Explain {topic} in a very simple term for beginners."
    )

    return {
        "explanation": response.content
    }

def clean_explanation(state: TechState):
    description = state["explanation"]

    cleaned = description.replace("*", "")

    return {
        "explanation": cleaned
    }


builder = StateGraph(TechState)

builder.add_node("explain_tech", explain_tech)
builder.add_node("clean_explanation", clean_explanation)

builder.add_edge(START, "explain_tech")
builder.add_edge("explain_tech", "clean_explanation")
builder.add_edge("clean_explanation", END)

graph = builder.compile()

topic = input("Enter a tech topic to explain: ")
result = graph.invoke(TechState(topic=topic, explanation=""))

print("\nEXPLANATION:")
print(result["explanation"])


