from dotenv import load_dotenv
load_dotenv()

import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

translate = PromptTemplate.from_template(
    "Translate the following into simple English:\n{topic}"
)

summarize = PromptTemplate.from_template(
    "Summarize this in 3 lines:\n{text}"
)

reformat = PromptTemplate.from_template(
    "Convert this into bullet points:\n{text}"
)

parser = StrOutputParser()

chain = (
    translate
    | llm
    | parser
    | (lambda text: {"text": text})
    | summarize
    | llm
    | parser
    | (lambda text: {"text": text})
    | reformat
    | llm
    | parser
)

topic = input("Enter a topic: ")

result = chain.invoke({"topic": topic})

print("\nFinal Output:\n")
print(result)