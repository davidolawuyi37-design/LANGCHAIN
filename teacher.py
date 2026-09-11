from langgraph.graph import StateGraph, START, END
from typing import TypedDict

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import SecretStr
import os

load_dotenv()


class StudyState(TypedDict):
    topic: str
    explanation: str


llm = ChatOpenAI(
    api_key=SecretStr(os.environ["DEEPSEEK_API_KEY"]),
    base_url="https://api.deepseek.com",
    model="deepseek-chat"
)


def explain_topic(state: StudyState):
    topic = state["topic"]

    response = llm.invoke(
        f"Explain {topic} in a very simple term for beginners."
    )

    return {
        "explanation": response.content
    }


def clean_explanation(state: StudyState):
    explanation = state["explanation"]

    cleaned = explanation.replace("*", "")

    return {
        "explanation": cleaned
    }


builder = StateGraph(StudyState)

builder.add_node("explain_topic", explain_topic)
builder.add_node("clean_explanation", clean_explanation)

builder.add_edge(START, "explain_topic")
builder.add_edge("explain_topic", "clean_explanation")
builder.add_edge("clean_explanation", END)

graph = builder.compile()


topic = input("Enter a topic to explain: ")

result = graph.invoke({
    "topic": topic,
    "explanation": ""
})


print("\nEXPLANATION:")
print(result["explanation"])