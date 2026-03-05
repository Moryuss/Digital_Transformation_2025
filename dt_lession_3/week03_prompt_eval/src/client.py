import os
from dotenv import load_dotenv

load_dotenv()


import re

def strip_thinking(text):
    # handles <think>...</think> with any whitespace/newlines
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    # handles unclosed <think> tag (model started thinking but didn't close)
    text = re.sub(r"<think>.*", "", text, flags=re.DOTALL)
    return text.strip()
# ── shared config defaults ────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "temperature": 0.6,
    "top_p": 0.95,
    "max_tokens": 1024,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}
def prompt_ollama(system_prompt, prompt, model="mistral", **config):
    from ollama import chat, ChatResponse

    options = {}
    if "temperature" in config:
        options["temperature"] = config["temperature"]
    if "top_p" in config:
        options["top_p"] = config["top_p"]
    if "max_tokens" in config:
        options["num_predict"] = config["max_tokens"]

    response: ChatResponse = chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt},
        ],
        options=options or None,
    )

    return strip_thinking(response.message.content)


def prompt_gpustack(system_prompt, prompt, model="qwen/qwen3", **config):
    from openai import OpenAI

    client = OpenAI(
        base_url="https://gpustack.ing.unibs.it/v1",
        api_key=os.environ["GPUSTACK_API_KEY"],
    )
    cfg = {**DEFAULT_CONFIG, **config}

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt},
        ],
        **cfg,
    )

    return strip_thinking(response.choices[0].message.content)


def prompt_groq(system_prompt, prompt, model="qwen/qwen3-32b", **config):
    from groq import Groq

    client = Groq()
    cfg = {**DEFAULT_CONFIG, **config}

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt},
        ],
        **cfg,
    )

    return strip_thinking(response.choices[0].message.content)


def prompt(system_prompt, prompt_text, model=None, backend="ollama", **config):
    backend = backend.lower()
    kwargs = dict(system_prompt=system_prompt, prompt=prompt_text, **config)
    if model:
        kwargs["model"] = model

    if backend == "ollama":
        return prompt_ollama(**kwargs)
    elif backend in ("gpustack", "openai"):
        return prompt_gpustack(**kwargs)
    elif backend == "groq":
        return prompt_groq(**kwargs)
    else:
        raise ValueError(f"Unknown backend '{backend}'. Choose: ollama | gpustack | groq")