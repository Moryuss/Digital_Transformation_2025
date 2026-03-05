from ollama import chat
from ollama import ChatResponse

def prompt(system_prompt, prompt, model="mistral"):
    response: ChatResponse = chat(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    )
    print("\nX=X=X=X=X=X=X=X= system_prompt =X=X=X=X=X=X=X=X\n")
    print(system_prompt)
    print("\nX=X=X=X=X=X=X=X= prompt =X=X=X=X=X=X=X=X\n")
    print(prompt)
    
    reasoning = getattr(response.message, "reasoning_content", None)
    if reasoning:
        print("\nX=X=X=X=X=X=X=X= THINKING-PROCESS =X=X=X=X=X=X=X=X\n")
        print(reasoning)

    print("\nX=X=X=X=X=X=X=X= RESPONSE =X=X=X=X=X=X=X=X\n")
    print(response.message.content)


system_prompt = " You are a degenerate"
prompt_message = "who are you?"
prompt(system_prompt, prompt_message)