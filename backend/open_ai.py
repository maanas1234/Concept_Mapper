from openai import OpenAI
import os
from dotenv import load_dotenv



client = OpenAI()

input = """Tell me about the best book ever written"""
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": input},
              {"role":"system","content":"You are an helpful assistant"}],
)
print(completion.choices[0].message.content) 