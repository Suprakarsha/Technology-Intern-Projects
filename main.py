from triage_agent import triage
from knowledge_agent import knowledge
from resolution_agent import resolve

print("=" * 50)
print("      TICKET RESOLVER SYSTEM")
print("=" * 50)

while True:

    ticket = input("\nEnter Ticket (exit to quit): ")

    if ticket.lower() == "exit":
        print("\nSystem Closed.")
        break

    # Agent 1
    ticket_data = triage(ticket)

    # Agent 2
    solution = knowledge(ticket_data)

    # Agent 3
    final_solution = resolve(solution)

    # Agent 4 (Review Agent)
    print("\n========== REVIEW AGENT ==========")
    print("Status : Ticket Processed Successfully")

    print("\nFinal Solution:")
    print(final_solution)