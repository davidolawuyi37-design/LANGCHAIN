from langgraph.graph import StateGraph, START, END
from typing import TypedDict

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import SecretStr
import os

load_dotenv()

class MusicState(TypedDict):
    genre: str
    description: str

llm = ChatOpenAI(
    api_key=SecretStr(os.environ["DEEPSEEK_API_KEY"]),
    base_url="https://api.deepseek.com",
    model="deepseek-chat"
)

def describe_music(state: MusicState):
    genre = state["genre"]
    
    response = llm.invoke(
        f"Describe the components of {genre} music in uncomplicated terms."
    )

    return {
        "description": response.content
    }

def clean_description(state: MusicState):
    description = state["description"]
    cleaned = description.replace("*", "")

    return {
        "description": cleaned
    }

builder = StateGraph(MusicState)

builder.add_node("describe_music", describe_music)
builder.add_node("clean_description", clean_description)

builder.add_edge(START, "describe_music")
builder.add_edge("describe_music", "clean_description")
builder.add_edge("clean_description", END)

graph = builder.compile()

genre = input("Enter a music genre to describe: ")
result = graph.invoke(MusicState(genre=genre, description=""))

print("\nDESCRIPTION:")
print(result["description"])    

