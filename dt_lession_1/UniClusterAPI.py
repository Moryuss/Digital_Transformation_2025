import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 

client = OpenAI(
    base_url="https://gpustack.ing.unibs.it/v1",
    api_key=os.environ["GPUSTACK_API_KEY"],)

def prompt(system_prompt, prompt, model="qwen/qwen3"):
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

# qwen3 Hugging Face/unsloth/Qwen3-4B-GGUF
# phi4-mini Hugging Face/unsloth/Phi-4-mini-instruct-GGUF
# phi4 Hugging Face/bartowski/phi-4-GGUF
# llama3.2 Hugging Face/bartowski/Llama-3.2-3B-Instruct-GGUF
# gpt-oss Hugging Face/unsloth/gpt-oss-20b-GGUF
# granite3.3 Hugging Face/ibm-granite/granite-3.3-2b-instruct-GGUF
# gemma3 Hugging Face/bartowski/google_gemma-3-1b-it-GGUF
system_prompt = " You are a helpful AI Assistant"
prompt_message = "Hello I'M Matteo"
prompt(system_prompt, prompt_message, model="phi4")
