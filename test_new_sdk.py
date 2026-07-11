from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6KomqQBT-xJ8SEaGtdN8qzG_Vn9ZKIQ6de3ZhkbcGMNJ"
)

try: 
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello!"
    )

    print("✅ Success!")
    print(response.text)

except Exception as e:
    print("❌ Error:")
    print(e)