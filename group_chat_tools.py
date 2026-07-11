# -----------------------------
# group_chat_tools.py
# Simple 3-Agent Group Chat
# -----------------------------

# -----------------------------
# Search Tool
# -----------------------------
def search_tool(query):
    knowledge = {
        "python": "Python is a high-level, interpreted programming language.",
        "ai": "Artificial Intelligence enables machines to perform tasks that normally require human intelligence.",
        "langgraph": "LangGraph is a framework for building stateful, multi-agent AI workflows.",
        "langchain": "LangChain helps developers build applications powered by Large Language Models."
    }

    query = query.lower()

    for key in knowledge:
        if key in query:
            return knowledge[key]

    return "No relevant information found."


# -----------------------------
# Planner Agent
# -----------------------------
def planner(user_input):
    print("\n========== Planner Agent ==========")
    print("Planning the task...")
    info = search_tool(user_input)
    print("Search Tool Result:", info)

    return info


# -----------------------------
# Coder Agent
# -----------------------------
def coder(info):
    print("\n========== Coder Agent ==========")

    answer = f"""
Answer:
{info}

This response was prepared using the Planner's search results.
"""

    print(answer)

    return answer


# -----------------------------
# Critic Agent
# -----------------------------
def critic(answer):
    print("\n========== Critic Agent ==========")

    print("Reviewing the answer...")

    if "No relevant information found" in answer:
        feedback = "The answer needs more information."
    else:
        feedback = "The answer looks good and is ready to present."

    print("Feedback:", feedback)

    return feedback


# -----------------------------
# Main Program
# -----------------------------
print("=" * 50)
print("      3-Agent Group Chat System")
print("=" * 50)

while True:

    user = input("\nEnter your question (or type 'exit'): ")

    if user.lower() == "exit":
        print("\nExiting Group Chat...")
        break

    planner_output = planner(user)

    coder_output = coder(planner_output)

    critic_output = critic(coder_output)

    print("\n========== Final Result ==========")
    print(coder_output)
    print("Critic:", critic_output)