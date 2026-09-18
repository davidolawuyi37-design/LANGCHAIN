from langgraph.graph import StateGraph, START, END
from typing import TypedDict

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import SecretStr
import os

load_dotenv()

class HouseState(TypedDict):
    house_type: str
    description: str

llm = ChatOpenAI(
    api_key=SecretStr(os.environ["DEEPSEEK_API_KEY"]),
    base_url="https://api.deepseek.com",
    model="deepseek-chat"
)

def describe_house(state: HouseState):
    house_type = state["house_type"]

    response = llm.invoke(
        f"Describe a {house_type} in a term for potential buyers. Talk about the pricing and everything that makes it unique. Make it sound appealing and interesting. Use a friendly tone."
    )

    return {
        "description": response.content
    }

def clean_description(state: HouseState):
    description = state["description"]

    cleaned = description.replace("*", "")

    return {
        "description": cleaned
    }

builder = StateGraph(HouseState)

builder.add_node("describe_house", describe_house)
builder.add_node("clean_description", clean_description)

builder.add_edge(START, "describe_house")
builder.add_edge("describe_house", "clean_description")
builder.add_edge("clean_description", END)

graph = builder.compile()

house_type = input("Enter a house type to describe: ")
result = graph.invoke(HouseState(house_type=house_type, description=""))

print("\nDESCRIPTION:")
print(result["description"])