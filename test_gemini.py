import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6KomqQBT-xJ8SEaGtdN8qzG_Vn9ZKIQ6de3ZhkbcGMNJ")

try:
    models = genai.list_models()
    print("✅ API Key Works!")
    for model in models:
        print(model.name)
except Exception as e:
    print("❌ Error:", e)