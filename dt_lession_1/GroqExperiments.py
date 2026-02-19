import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

def prompt(system_prompt, prompt, model="qwen/qwen3-32b", **config):
    """
    Function to send a prompt to the model with customizable configuration parameters.
    
    :param system_prompt: The system's prompt to define its behavior.
    :param prompt: The user's input message.
    :param model: The model to use (default is 'qwen/qwen3-32b').
    :param config: Additional configuration parameters (temperature, top_p, max_tokens, etc.)
    :return: None
    """
    client = Groq()

    # Default configuration
    default_config = {
        "temperature": 0.6,
        "top_p": 0.95,
        "max_tokens": 1024,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    # Update default config with the user-provided config
    config = {**default_config, **config}

    # Send the completion request
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        **config
    )

    # Output formatting for easier comparison
    print("\nX=X=X=X=X=X=X=X= SYSTEM PROMPT =X=X=X=X=X=X=X=X\n")
    print(system_prompt)
    print("\nX=X=X=X=X=X=X=X= USER PROMPT =X=X=X=X=X=X=X=X\n")
    print(prompt)

    # Optionally print reasoning content (if available)
    reasoning1 = getattr(response.choices[0].message, "reasoning_content", None)

    if reasoning1:
        print("\nX=X=X=X=X=X=X=X= THINKING-PROCESS =X=X=X=X=X=X=X=X\n")
        print(reasoning1)



    print("\nX=X=X=X=X=X=X=X= RESPONSE =X=X=X=X=X=X=X=X\n")
    print(response.choices[0].message.content)


# Example usage with different config
system_prompt = "You are a helpful AI Assistant"


# Config 1
print("\n##config 1")
prompt_message_1 = "how do i remove a file from a commit git?"
config_1 = {"temperature": 2, "top_p": 0.95, "max_tokens": 800}
prompt(system_prompt, prompt_message_1, **config_1)

# Config 2
print("\n##config 2")
prompt_message_2 = "how do i remove a file from a commit git?"
config_2 = {"temperature": 0.5, "top_p": 0.95, "max_tokens": 1024, "presence_penalty": 1}
prompt(system_prompt, prompt_message_2, **config_2)
