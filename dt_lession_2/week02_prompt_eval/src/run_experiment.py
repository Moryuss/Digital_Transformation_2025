from client import *
from datetime import datetime
import json
import pandas as pd
from prompts import zero_shot_instruction, few_shot_instruction, role_based_instruction, constrained_instruction

import os

# -- Validation methods

def count_words(text):
    if text is None:
        return 0
    return len(text.split())

def check_keywords(text, keywords=["1900", "application"]):
    if text is None:
        return 0
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw in text_lower)

'''
TASK: Explaining the possible different uses of elements"
'''

# Creation of the dirs
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, "data", "inputs.json")
results_path = os.path.join(base_dir, "results", "outputs.csv")

with open(data_path, "r") as f:
    inputs = json.load(f)
results = []


TEMPERATURE = 0.7
TOP_P = 0.95
MAX_TOKENS = 800
# MODEL = "mistral:latest"
MODEL = "openai/gpt-oss-20b"
BACKEND = "groq"

for topic in inputs:
    print(f"Topic - {topic}")

    # --- zero shot ---
    print("Zero Shot query")
    response = prompt(
        system_prompt="",
        prompt_text=zero_shot_instruction(topic),
        backend=BACKEND,
        model=MODEL,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        max_tokens=MAX_TOKENS,
    )
    results.append({
        "input": topic,
        "variant": "zero_shot",
        "raw_output": response,
        "parse_success": None,  # not applicable
        "schema_valid": None,
        "word_count": count_words(response),
        "keywords_found": check_keywords(response),
    })

    # --- few shot ---
    print("Few Shot query")
    response = prompt(
        system_prompt="",
        prompt_text=few_shot_instruction(topic),
        backend=BACKEND,
        model=MODEL,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        max_tokens=MAX_TOKENS,
    )
    results.append({
        "input": topic,
        "variant": "few_shot",
        "raw_output": response,
        "parse_success": None,
        "schema_valid": None,
        "word_count": count_words(response),
        "keywords_found": check_keywords(response),
    })

    # --- role based ---
    print("role based query")
    system_msg, user_msg = role_based_instruction(topic)
    response = prompt(
        system_prompt=system_msg,
        prompt_text=user_msg,
        backend=BACKEND,
        model=MODEL,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        max_tokens=MAX_TOKENS,
    )
    results.append({
        "input": topic,
        "variant": "role_based",
        "raw_output": response,
        "parse_success": None,
        "schema_valid": None,
        "word_count": count_words(response),
        "keywords_found": check_keywords(response),
    })

    # --- constrained ---
    print("Constrained query")
    response = prompt(
        system_prompt="",
        prompt_text=constrained_instruction(topic),
        backend=BACKEND,
        model=MODEL,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        max_tokens=MAX_TOKENS,
    )
    ## --- CHECK VALIDITY OF JSON ---
    if response is None:
        parse_success = False
        schema_valid = False
    else:
        try:
            parsed = json.loads(response)
            parse_success = True
            required_fields = ["element", "industrial_uses", "medical_uses", "everyday_uses"]
            schema_valid = all(field in parsed for field in required_fields)
        except json.JSONDecodeError:
            parse_success = False
            schema_valid = False

    results.append({
        "input": topic,
        "variant": "constrained",
        "raw_output": response,
        "parse_success": parse_success,
        "schema_valid": schema_valid,
        "word_count": count_words(response),
        "keywords_found": check_keywords(response),
    })

# save results
df = pd.DataFrame(results)

timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
results_path = os.path.join(base_dir, "results", f"outputs_{timestamp}.json")

with open(results_path, "w") as f:
    json.dump(json.loads(df.to_json(orient="records")), f, indent=2)


# save constrainied results
constrained_parsed = []

for row in results:
    if row["variant"] == "constrained" and row["parse_success"]:
        constrained_parsed.append(json.loads(row["raw_output"]))

parsed_path = os.path.join(base_dir, "results", f"parsed_{timestamp}.json")
with open(parsed_path, "w") as f:
    json.dump(constrained_parsed, f, indent=2)
#

print(df)