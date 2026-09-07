# ASSIGNMENT:Create three nodes
#1: My name is David
#2. I am learning AI engineering
#3. I am learning Langgraph. 
# Connect them in sequence & print the final message.

# Exercise: Modify the graph so that each node appends a new sentence to the existing message instead of replacing it.

from typing import TypedDict # typing is used to describe the kinds of data our program expects. TypedDict is used to describe a dictionary with specific keys and value types. In this case, we are defining a State class that has a single key "message" of type str.
from langgraph.graph import StateGraph, START, END  #The langgraph.graph module provides the StateGraph class, which is used to create and manage a graph of nodes. The START and END constants are used to define the starting and ending points of the graph.

# Create State class to hold the shared information between nodes.
class State(TypedDict):
    message: str

# Create nodes
def node_x(state):
    return {
        "message":  "My name is David. " 
    }

def node_y(state):
    return {
        "message": state["message"] + "I am learning AI engineering. " 
    }

def node_z(state):
    return {
        "message": state["message"] + "I am learning Langgraph."
    }

# Build the graph
builder = StateGraph(State)
builder.add_node("node_x", node_x)
builder.add_node("node_y", node_y)
builder.add_node("node_z", node_z)

# Connect the nodes in sequence
builder.add_edge(START, "node_x")
builder.add_edge("node_x", "node_y")
builder.add_edge("node_y", "node_z")
builder.add_edge("node_z", END)

# Compile the graph
compiled_graph = builder.compile()

# Invoke the graph (provide an initial State with the required "message" key)
end_result = compiled_graph.invoke({"message": ""})

# Print the final message
print(end_result["message"])

# Student = {
# "age": 20, 
# "name": "David"
#   }

## Student = {
# "age": int
# "name": str
#   }

# Explanation according to the question, the final message is a concatenation of the messages from each node, resulting in: "My name is David. I am learning AI engineering. I am learning Langgraph."



# Routing and looping in LangGraph
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

# Step 1: Define the information that will move through the graph
class StudentState(TypedDict):
    topic: str
    score: int
    attempts: int
    history:str

# Step 2: First node: teach the student
def teach_student(state: StudentState):
    print(f"Teaching the student about {state['topic']}.")

    return {
        "history": state["history"] + "  -> TEACH"
    }

# Step 3: Second node: simulate a quiz for the student
def quiz_node(state: StudentState):
    print("Student is taking the quiz...")

    # For learning purposes, the score increases after each attempt.
    new_score = state["score"] + 20

    return{
        "score": new_score,
        "attempts": state["attempts"] + 1,
        "history": state["history"] + " -> QUIZ"
    }

# Step 4: Third node: Check if the student has passed the topic
def check_result_node(state: StudentState): 
    print(f"Checking result, Current score: {state['score']}")

    return {
        "history": state["history"] + " -> CHECK"

    }

# Step 5: Fourth node: Decide whether to loop back or finish.
def choose_next_stop(
        state: StudentState
) -> Literal["teach", "quiz", "end"]:
    
    # Safety condition to prevent an endless loop
    if state["attempts"] >= 5:
        return "end"
    
    # Very low score means the student should go back to the teaching 
    if state["score"] < 40:
        return "teach"
    
    #Medium score means the student should retry the quiz
    if state["score"] < 80:
        return "quiz"
    # A score of 70 or above means the student has passed, ends the workflow
    return "end"

# 6. Create the graph builder
builder = StateGraph(StudentState)

# 7. Register the nodes
builder.add_node("teach", teach_student)
builder.add_node("quiz", quiz_node)
builder.add_node("check_result", check_result_node)

# 8. Add the normal edges
builder.add_edge(START, "teach")
builder.add_edge("teach", "quiz")
builder.add_edge("quiz", "check_result")

# 9. Add the conditional movement after checking the result
builder.add_conditional_edges(
    "check_result",
    choose_next_stop,
    {
        "teach": "teach",
        "quiz": "quiz",
        "end": END
    }
)

# 10. Compile the graph
learning_graph = builder.compile()

# 11. Run the graph
result = learning_graph.invoke({
    "topic": "Genetics",
    "score": 0,
    "attempts": 0,
    "history": "START"
})

# 12. Display the result
print("\nFinal Result")
print("Topic:", result["topic"])
print("Score:", result["score"])
print("Attempts:", result["attempts"])
print("History:", result["history"])
    