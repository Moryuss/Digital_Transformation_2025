import os
from dotenv import load_dotenv

load_dotenv()

# ── pretty printer ────────────────────────────────────────────────────────────

def _print_result(system_prompt, prompt, response_content, reasoning=None):
    print("\nX=X=X=X=X=X=X=X= SYSTEM PROMPT =X=X=X=X=X=X=X=X\n")
    print(system_prompt)
    print("\nX=X=X=X=X=X=X=X= USER PROMPT =X=X=X=X=X=X=X=X\n")
    print(prompt)
    if reasoning:
        print("\nX=X=X=X=X=X=X=X= THINKING-PROCESS =X=X=X=X=X=X=X=X\n")
        print(reasoning)
    print("\nX=X=X=X=X=X=X=X= RESPONSE =X=X=X=X=X=X=X=X\n")
    print(response_content)


# ── shared config defaults ────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "temperature": 0.6,
    "top_p": 0.95,
    "max_tokens": 1024,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

# ── backends ──────────────────────────────────────────────────────────────────

def prompt_ollama(system_prompt, prompt, model="mistral", **config):
    """Talk to a local Ollama model. Extra config keys are ignored (Ollama
    supports only a subset of generation params via the `options` dict)."""
    from ollama import chat, ChatResponse

    # Ollama accepts generation options separately
    options = {}
    if "temperature" in config:
        options["temperature"] = config["temperature"]
    if "top_p" in config:
        options["top_p"] = config["top_p"]
    if "max_tokens" in config:
        options["num_predict"] = config["max_tokens"]   # Ollama's name

    response: ChatResponse = chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt},
        ],
        options=options or None,
    )

    reasoning = getattr(response.message, "reasoning_content", None)
    _print_result(system_prompt, prompt, response.message.content, reasoning)


def prompt_gpustack(system_prompt, prompt, model="qwen/qwen3", **config):
    """Talk to a GPUStack endpoint (OpenAI-compatible)."""
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

    reasoning = getattr(response.choices[0].message, "reasoning_content", None)
    _print_result(system_prompt, prompt, response.choices[0].message.content, reasoning)


def prompt_groq(system_prompt, prompt, model="qwen/qwen3-32b", **config):
    """Talk to a Groq-hosted model."""
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

    reasoning = getattr(response.choices[0].message, "reasoning_content", None)
    _print_result(system_prompt, prompt, response.choices[0].message.content, reasoning)


# ── unified entry-point ───────────────────────────────────────────────────────

def prompt(system_prompt, prompt_text, model=None, backend="ollama", **config):
    """
    Unified prompt function.

    Parameters
    ----------
    system_prompt : str
    prompt_text   : str
    model         : str | None   – uses each backend's default when None
    backend       : "ollama" | "gpustack" | "groq"
    **config      : temperature, top_p, max_tokens, frequency_penalty,
                    presence_penalty  (ignored silently when unsupported)
    """
    backend = backend.lower()
    kwargs = dict(system_prompt=system_prompt, prompt=prompt_text, **config)
    if model:
        kwargs["model"] = model

    if backend == "ollama":
        prompt_ollama(**kwargs)
    elif backend in ("gpustack", "openai"):
        prompt_gpustack(**kwargs)
    elif backend == "groq":
        prompt_groq(**kwargs)
    else:
        raise ValueError(f"Unknown backend '{backend}'. Choose: ollama | gpustack | groq")

