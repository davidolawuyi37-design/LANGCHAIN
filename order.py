from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END


class OrderState(TypedDict):
    item: str
    paid: bool
    payment_attempts: int
    status: str


def receive_order(state: OrderState):
    print(f"Order received for: {state['item']}")

    return {
        "status": "order_received"
    }


def check_payment(state: OrderState):
    print("Checking payment...")

    return {
        "status": "payment_checked"
    }


def retry_payment(state: OrderState):
    print("Payment failed. Trying payment again.")

    new_attempts = state["payment_attempts"] + 1

    # Simulate successful payment on second attempt
    if new_attempts >= 2:
        payment_status = True
    else:
        payment_status = False

    return {
        "paid": payment_status,
        "payment_attempts": new_attempts,
        "status": "payment_retried"
    }


def prepare_order(state: OrderState):
    print("Payment successful.")
    print("Preparing order...")

    return {
        "status": "order_ready"
    }


def decide_payment_route(
    state: OrderState
) -> Literal["prepare", "retry"]:

    if state["paid"]:
        return "prepare"

    return "retry"


builder = StateGraph(OrderState)

builder.add_node("receive_order", receive_order)
builder.add_node("check_payment", check_payment)
builder.add_node("retry_payment", retry_payment)
builder.add_node("prepare_order", prepare_order)


builder.add_edge(START, "receive_order")

builder.add_edge(
    "receive_order",
    "check_payment"
)


builder.add_conditional_edges(
    "check_payment",
    decide_payment_route,
    {
        "prepare": "prepare_order",
        "retry": "retry_payment"
    }
)


builder.add_edge(
    "retry_payment",
    "check_payment"
)

builder.add_edge(
    "prepare_order",
    END
)


graph = builder.compile()


result = graph.invoke({
    "item": "Laptop",
    "paid": False,
    "payment_attempts": 0,
    "status": ""
})


print("\nFINAL RESULT")
print(result)