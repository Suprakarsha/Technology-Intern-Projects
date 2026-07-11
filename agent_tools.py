from langchain_core.tools import tool

# Tool 1: Calculator
@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid expression"

# Tool 2: String Reverser
@tool
def reverse_string(text: str) -> str:
    """Reverse the given string."""
    return text[::-1]


while True:
    print("\nChoose a tool:")
    print("1. Calculator")
    print("2. Reverse String")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        expr = input("Enter expression: ")
        print("Result:", calculator.invoke(expr))

    elif choice == "2":
        text = input("Enter text: ")
        print("Result:", reverse_string.invoke(text))

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")