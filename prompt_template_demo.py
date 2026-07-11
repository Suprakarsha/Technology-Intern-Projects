from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} in simple words."
)

formatted_prompt = prompt.invoke(
    {
        "topic": "LangChain"
    }
)

print(formatted_prompt.text)