import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv() 
def prompt(system_prompt, prompt, model="qwen/qwen3-32b"):
    client = Groq()
    response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ],
    temperature=0.6,
    top_p=0.95,
    max_tokens=1024,
    frequency_penalty=0,
    presence_penalty=0,
    )
    print("\nX=X=X=X=X=X=X=X= system_prompt =X=X=X=X=X=X=X=X\n")
    print(system_prompt)
    print("\nX=X=X=X=X=X=X=X= prompt =X=X=X=X=X=X=X=X\n")
    print(prompt)
    
    reasoning = getattr(response.choices[0].message, "reasoning_content", None)
    if reasoning:
        print("\nX=X=X=X=X=X=X=X= THINKING-PROCESS =X=X=X=X=X=X=X=X\n")
        print(reasoning)

    print("\nX=X=X=X=X=X=X=X= RESPONSE =X=X=X=X=X=X=X=X\n")
    print(response.choices[0].message.content)


system_prompt = " You are a helpful AI Assistant"
prompt_message = "Hello I'M Matteo"
prompt(system_prompt, prompt_message)

