from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class MovieRecommendationState(TypedDict):
    user_options: str
    recommended_movies: list[str]
    

def receive_genre(state: MovieRecommendationState):
    print("Fetching user's movie genre...")
    genre = input("Please enter your preferred movie genre: ").strip().lower()
    return {
        "user_options": genre
    }


def check_genre(state: MovieRecommendationState):   
    print("Checking user's preferred movie genre...")

    genre = state["user_options"]

    return {
        "user_options": genre
    }

def route_genre( 
    state: MovieRecommendationState
) -> Literal["action", "comedy", "unknown"]:

    genre = state["user_options"]

    if genre == "action":
        return "action"
    elif genre == "comedy":
        return "comedy"
    else:
        return "unknown"


def comedy_recommendation(state: MovieRecommendationState):
    print("Recommending comedy movies...")
    return {
        "recommended_movies": ["Groundhog Day", "The Hangover", "Airplane!", "Hit Man"]
    }

def action_recommendation(state: MovieRecommendationState):
    print("Recommending action movies...")
    return {
        "recommended_movies": ["Extraction", "Mad Max: Fury Road", "John Wick", "The Equalizer"]
    }

def general_recommendation(state: MovieRecommendationState):
    print("Recommending general movies...")
    return {
        "recommended_movies": ["The Shawshank Redemption", "Forrest Gump", "The Man From Nowhere", "Hard Boiled"]
    }

builder = StateGraph(MovieRecommendationState)
builder.add_node("receive_genre", receive_genre)
builder.add_node("check_genre", check_genre)
builder.add_node("comedy_recommendation", comedy_recommendation)
builder.add_node("action_recommendation", action_recommendation)
builder.add_node("general_recommendation", general_recommendation)

builder.add_conditional_edges(
    "check_genre",
    route_genre,
    {
        "action": "action_recommendation",
        "comedy": "comedy_recommendation",
        "unknown": "general_recommendation"
    }
)

builder.add_edge(START, "receive_genre")

builder.add_edge("receive_genre", "check_genre")

builder.add_edge("action_recommendation", END)

builder.add_edge("comedy_recommendation", END)

builder.add_edge("general_recommendation", END)

graph = builder.compile()

outcome = graph.invoke({
    "user_options": "",
    "recommended_movies": []
})

print("\nFINAL RESULT")
print(f"Genre: {outcome['user_options']}")
print("Recommended movies: ")

for movie in outcome["recommended_movies"]:
    print(f"- {movie}")