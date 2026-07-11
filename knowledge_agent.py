from rag_retriever import retrieve

def knowledge(ticket):

    print("\n========== KNOWLEDGE AGENT ==========")

    solution = retrieve(ticket)

    return solution