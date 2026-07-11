from dotenv import load_dotenv
import os
from typing import TypedDict

load_dotenv()

# -------------------------
# Check API Key
# -------------------------
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

print("✅ API Key Loaded Successfully!")

# -------------------------
# LangChain Imports
# -------------------------
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# -------------------------
# LangGraph Imports
# -------------------------
from langgraph.graph import StateGraph, START, END

# -------------------------
# Graph State
# -------------------------
class GraphState(TypedDict):
    question: str
    context: str
    answer: str

# -------------------------
# Load PDF
# -------------------------
loader = PyPDFLoader("data/company_faq.pdf")
docs = loader.load()

# -------------------------
# Split Documents
# -------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

documents = splitter.split_documents(docs)

# -------------------------
# Embeddings
# -------------------------
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001"
)

# -------------------------
# FAISS Vector Store
# -------------------------
db = FAISS.from_documents(
    documents,
    embeddings
)

retriever = db.as_retriever()

# -------------------------
# Gemini LLM
# -------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# =====================================================
# RESEARCHER AGENT
# =====================================================

def researcher(state: GraphState):

    print("\n🔎 Researcher Agent Working...")

    docs = retriever.invoke(state["question"])

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return {
        **state,
        "context": context
    }

# =====================================================
# WRITER AGENT
# =====================================================

def writer(state: GraphState):

    print("✍ Writer Agent Working...")

    prompt = f"""
You are an AI assistant.

Answer ONLY using the context below.

Context:
{state["context"]}

Question:
{state["question"]}

If the answer is not found in the context,
reply with:

"I couldn't find that information in the document."
"""

    response = llm.invoke(prompt)

    return {
        **state,
        "answer": response.content
    }

# =====================================================
# BUILD LANGGRAPH
# =====================================================

builder = StateGraph(GraphState)

builder.add_node(
    "Researcher",
    researcher
)

builder.add_node(
    "Writer",
    writer
)

builder.add_edge(
    START,
    "Researcher"
)

builder.add_edge(
    "Researcher",
    "Writer"
)

builder.add_edge(
    "Writer",
    END
)

graph = builder.compile()

# =====================================================
# PRINT GRAPH
# =====================================================

print("\n==============================")
print("LangGraph Diagram")
print("==============================\n")

print(graph.get_graph().draw_mermaid())

# =====================================================
# CHAT LOOP
# =====================================================

while True:

    question = input("\nAsk a Question (type 'exit' to quit): ")

    if question.lower() == "exit":
        print("\nGoodbye!")
        break

    result = graph.invoke(
        {
            "question": question,
            "context": "",
            "answer": ""
        }
    )

    print("\n==============================")
    print("Final Answer")
    print("==============================\n")

    print(result["answer"])