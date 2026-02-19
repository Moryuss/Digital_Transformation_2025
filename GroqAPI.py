import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv() 
def prompt(message, model="qwen/qwen3-32b"):
    client = Groq()
    completion = client.chat.completions.create(
        model=model,
        messages=[
          {
            "role": "user",
            "content": message
          }
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        reasoning_effort="default",
        stream=True,
        stop=None
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")


prompt("Hello i'm Matteo")
