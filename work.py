from  langgraph.graph import StateGraph, START, END
from typing import TypedDict

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv 
from pydantic import SecretStr
import os

load_dotenv()

class FruitState(TypedDict):
    fruit: str
    description: str

llm = ChatOpenAI(
    api_key=SecretStr(os.environ["DEEPSEEK_API_KEY"]),
    base_url="https://api.deepseek.com",
    model="deepseek-chat"
)

def describe_fruit(state: FruitState):
    fruit = state["fruit"]

    response = llm.invoke(
        f"Describe {fruit} using this following terms: Its background,botanical name, usefulness, e.t.c."
    )

    return {
        "description": response.content
    }


def clean_explanation(state: FruitState):
    explanation = state["description"]

    cleaned = explanation.replace("*", "")

    return {
        "description": cleaned
    }

builder = StateGraph(FruitState)

builder.add_node("describe_fruit", describe_fruit)
builder.add_node("clean_explanation", clean_explanation)

builder.add_edge(START, "describe_fruit")
builder.add_edge("describe_fruit", "clean_explanation")
builder.add_edge("clean_explanation", END)

graph = builder.compile()

fruit = input("Enter a fruit to describe: ")
result = graph.invoke(FruitState(fruit=fruit, description=""))


print("\nDESCRIPTION:")
print(result["description"])