import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is loaded
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found. Please check your .env file."
    )

print("✅ API Key Loaded Successfully!")

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

# -----------------------------
# Load PDF
# -----------------------------
loader = PyPDFLoader("data/company_faq.pdf")
docs = loader.load()

# -----------------------------
# Split into chunks
# -----------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

documents = splitter.split_documents(docs)

# -----------------------------
# Create Embeddings
# -----------------------------
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=api_key
)

# -----------------------------
# Create Vector Store
# -----------------------------
db = FAISS.from_documents(documents, embeddings)

retriever = db.as_retriever()

# -----------------------------
# Gemini Model
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0
)

# -----------------------------
# Prompt Template
# -----------------------------
prompt = ChatPromptTemplate.from_template("""
Answer ONLY using the context below.

<context>
{context}
</context>

Question:
{input}
""")

# -----------------------------
# Create Chains
# -----------------------------
document_chain = create_stuff_documents_chain(
    llm,
    prompt
)

retrieval_chain = create_retrieval_chain(
    retriever,
    document_chain
)

# -----------------------------
# Chat Loop
# -----------------------------
while True:
    question = input("\nAsk a question (type 'exit' to quit): ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    response = retrieval_chain.invoke(
        {"input": question}
    )

    print("\nAnswer:\n")
    print(response["answer"])

    print("\nSources:")
    for doc in response["context"]:
        print("Page:", doc.metadata.get("page"))