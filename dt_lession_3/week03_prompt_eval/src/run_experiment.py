from client import *
from datetime import datetime
import json
import pandas as pd
import os


# Creation of the dirs
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, "data", "inputs.json")
results_path = os.path.join(base_dir, "results", "outputs.csv")


TEMPERATURE = 0.7
TOP_P = 0.95
MAX_TOKENS = 800
# MODEL = "mistral:latest"
MODEL = "openai/gpt-oss-20b"
BACKEND = "groq"

prompt_text = "Hello"

response = prompt(
    system_prompt="",
    prompt_text=(prompt_text),
    backend=BACKEND,
    model=MODEL,
    temperature=TEMPERATURE,
    top_p=TOP_P,
    max_tokens=MAX_TOKENS,
)



print(response)