from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

history = []

print("Type 'exit' to quit.\n")

while True:

    user = input("You : ")

    if user.lower() == "exit":
        break

    history.append(HumanMessage(content=user))

    response = llm.invoke(history)

    print("Bot :", response.content)

    history.append(AIMessage(content=response.content))