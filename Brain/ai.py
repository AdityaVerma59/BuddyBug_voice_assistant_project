# Brain/ai.py
import os
from openai import OpenAI
from config import HF_TOKEN

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

def ask_ai(query):
    """
    Sends query to Hugging Face gpt model and returns the response text
    """
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b:cerebras",
            messages=[{"role": "user", "content": query}],
        )
        # Hugging Face returns a ChatCompletionMessage object
        return completion.choices[0].message.content
    except Exception as e:
        return f"I couldn't get a response from the AI model: {e}"
