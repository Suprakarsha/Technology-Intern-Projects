from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# -------------------------
# State
# -------------------------
class GraphState(TypedDict):
    user_input: str
    intent: str
    response: str


# -------------------------
# Intent Classifier
# -------------------------
def classify_intent(state: GraphState):
    text = state["user_input"].lower()

    if "?" in text:
        state["intent"] = "question"

    elif any(word in text for word in ["create", "build", "write", "make", "do"]):
        state["intent"] = "task"

    else:
        state["intent"] = "chitchat"

    return state


# -------------------------
# Question Handler
# -------------------------
def question_handler(state: GraphState):
    state["response"] = "This looks like a question."
    return state


# -------------------------
# Task Handler
# -------------------------
def task_handler(state: GraphState):
    state["response"] = "This looks like a task."
    return state


# -------------------------
# Chitchat Handler
# -------------------------
def chitchat_handler(state: GraphState):
    state["response"] = "This looks like casual conversation."
    return state


# -------------------------
# Routing Function
# -------------------------
def route(state: GraphState):

    if state["intent"] == "question":
        return "question"

    elif state["intent"] == "task":
        return "task"

    return "chitchat"


# -------------------------
# Build Graph
# -------------------------
builder = StateGraph(GraphState)

builder.add_node("classifier", classify_intent)
builder.add_node("question", question_handler)
builder.add_node("task", task_handler)
builder.add_node("chitchat", chitchat_handler)

builder.add_edge(START, "classifier")

builder.add_conditional_edges(
    "classifier",
    route,
    {
        "question": "question",
        "task": "task",
        "chitchat": "chitchat",
    },
)

builder.add_edge("question", END)
builder.add_edge("task", END)
builder.add_edge("chitchat", END)

# -------------------------
# Compile Graph
# -------------------------
graph = builder.compile()

# -------------------------
# Print Mermaid Diagram
# -------------------------
print("\n=== Graph Diagram ===")
print(graph.get_graph().draw_mermaid())

# -------------------------
# Test Once
# -------------------------
result = graph.invoke(
    {
        "user_input": "Hello LangGraph",
        "intent": "",
        "response": "",
    }
)

print("\nTest Result:")
print(result)

# -------------------------
# Chat Loop
# -------------------------
while True:

    user = input("\nYou: ")

    if user.lower() == "exit":
        break

    result = graph.invoke(
        {
            "user_input": user,
            "intent": "",
            "response": "",
        }
    )

    print("\nIntent :", result["intent"])
    print("Response:", result["response"])