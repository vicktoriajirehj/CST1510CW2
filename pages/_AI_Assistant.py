import os
from openai import OpenAI

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def ask_ai(promt):
    try:
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages =[
                {"role": "system", "content": "You are an analytical AI Assistant in a cybersecurity/data/IT intelligence platform. "},
                {"role": "user", "content": promt}
            ],
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"AI error: {e}"