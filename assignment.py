from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class ATMState(TypedDict):
    balance : float
    withdrawal : float
    message : str
    status : str

def check_balance(state: ATMState):
    if state["withdrawal"] <= 0:
        return {"status": "invalid"}

    if state["withdrawal"] > state["balance"]: 
        return {"status" : "insufficient"}
    return {"status": "approved"}

def withdraw(state: ATMState):
    remaining = state["balance"] - state["withdrawal"]

    return {
        "balance": remaining,
        "message": "Withdrawal successful"
    }

def insufficient_balance(state: ATMState):
    return {
        "message": "Insufficient balance"
    }

def invalid_amount(state: ATMState):
    return {
        "message": "Invalid withdrawal amount"
    }

def route_after_check(state: ATMState) -> Literal[
    "withdraw",
    "insufficient_balance",
    "invalid_amount"
]:
    if state["status"] == "approved":
        return "withdraw"

    elif state["status"] == "insufficient":
        return "insufficient_balance"

    else:
        return "invalid_amount"

builder = StateGraph(ATMState)
builder.add_node("check_balance", check_balance)
builder.add_node("withdraw", withdraw)
builder.add_node("insufficient_balance", insufficient_balance)
builder.add_node("invalid_amount", invalid_amount)

builder.add_edge(START, "check_balance")

builder.add_conditional_edges(
    "check_balance",
    route_after_check
)

builder.add_edge("withdraw", END)
builder.add_edge("insufficient_balance", END)
builder.add_edge("invalid_amount", END)

graph = builder.compile()

result = graph.invoke({
    "balance": 5000,
    "withdrawal": 2000,
    "message": "",
    "status": ""
})

print("\nFINAL RESULT")
print(result["message"])
print(f"Remaining balance: {result['balance']}")

result = graph.invoke({
    "balance": 5000,
    "withdrawal": 7000,
    "message": "",
    "status": ""
})

print("\nFINAL RESULT")
print(result["message"])

result = graph.invoke({
    "balance": 5000,
    "withdrawal": 0,
    "message": "",
    "status": ""
})

print("\nFINAL RESULT")
print(result["message"])