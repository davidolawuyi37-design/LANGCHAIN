from typing import TypedDict, Literal # Literal means funtion can only return from the given options.
from langgraph.graph import StateGraph, START, END # Stategraph is a major tool used to create langgraph workfllows and it shares similarities with state machine. START and END are used to define the start and end of the workflow.


class StudyState(TypedDict): # typedict defines the type of data that can be stored in the state.
    topic: str
    lesson: str
    question: str
    student_answer: str
    correct_answer: str
    attempts: int
    result: str


def teach(state: StudyState):

    lesson = (
        f"{state['topic']} is an important Python concept. "
        " A function is a reusable block of code that performs a specific task."
    )

    print("\nLesson:")
    print(lesson)

    return {
        "lesson": lesson
    }


def create_quiz(state: StudyState):
    question = "which keyword is used to create a function in Python?"
    correct_answer = "def"

    print("\nQUIZ")
    print(question)

    answer = input("Your answer: ")

    return {
        "question": question,
        "correct_answer": correct_answer,
        "student_answer": answer,
        "attempts": state["attempts"] + 1
    }


def check_answer(state: StudyState):

    student_answer = state["student_answer"].strip().lower()
    correct_answer = state["correct_answer"].lower()

    if student_answer == correct_answer:
        result = "correct"
        print("\nCorrect! Well done.")

    else:
        result = "wrong"
        print("\nThat answer is not correct.")

    return {
        "result": result
    }


def explain_again(state: StudyState):

    print("\nLET'S EXPLAIN IT AGAIN")

    explanation = (
        "when we want to create a function in Python, "
        "we begin with the keyword 'def', "
        "For example: def greet():"
    )

    print(explanation)

    return {
        "lesson": explanation
    }


def decide_next_step(
        state: StudyState

) -> Literal["finish", "explain_again"]:

    if state["result"] == "correct":
        return "finish"

    return "explain_again"


builder = StateGraph(StudyState)

builder.add_node("teach", teach)
builder.add_node("create_quiz", create_quiz)
builder.add_node("check_answer", check_answer)
builder.add_node("explain_again", explain_again)

builder.add_edge(START, "teach") # edges connects the nodes together to form a workflow. The first edge connects the START node to the teach node, which means that the workflow will start with the teach function..
builder.add_edge("teach", "create_quiz")
builder.add_edge("create_quiz", "check_answer")

builder.add_conditional_edges( # 
    "check_answer",
    decide_next_step,
    {
        "finish": END,
        "explain_again": "explain_again"
    }
)

builder.add_edge(
    "explain_again",
    "create_quiz"
)

graph = builder.compile()

final_state = graph.invoke({
    "topic": "python functions",
    "lesson": "",
    "question": "",
    "student_answer": "",
    "correct_answer": "",
    "attempts": 0,
    "result": ""
})

print("\nSESSION COMPLETED")
print("Attempts:", final_state["attempts"])