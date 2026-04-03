from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b:free:online",
    messages=[
        {"role": "user", "content": "Tell me the latest news of claude code?Summarize in 3 lines."}
    ]
)

print(response.choices[0].message.content)