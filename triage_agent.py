from rag_retriever import retrieve

def triage(ticket):
    print("\n=== TRIAGE AGENT ===")
    print("Ticket:", ticket)

    result = retrieve(ticket)

    return result