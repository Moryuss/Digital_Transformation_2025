LIMIT_WORDS = "Do not write more than 50 words."
TIME = "1900"
LIMIT__TIME_FREEDOM = f"Talk only about uses discovered before {TIME}."

def zero_shot_instruction(topic):
    return f"Explain the possible uses of the element {topic}. {LIMIT_WORDS} {LIMIT__TIME_FREEDOM}"

def few_shot_instruction(topic):
    return f"""Here are some examples of element use explanations:

Element: Hydrogen
Uses: Hydrogen is used as a rocket fuel, in the production of ammonia for fertilizers, and in fuel cells to generate electricity.

Element: Carbon
Uses: Carbon is used in steel production, as graphite in pencils, as diamonds in cutting tools, and as a base for all organic chemistry.

Now explain the possible uses of the element: {topic}. {LIMIT_WORDS} {LIMIT__TIME_FREEDOM}"""

def role_based_instruction(topic):
    system = "You are an expert chemist and science communicator. You explain the real-world uses of chemical elements in a clear, precise, and engaging way, covering industrial, medical, and everyday applications."
    user = f"Explain the possible uses of the element {topic}. {LIMIT_WORDS} {LIMIT__TIME_FREEDOM}"
    return system, user

def constrained_instruction(topic):
    return f"""Explain the possible uses of the element {topic}. {LIMIT_WORDS} {LIMIT__TIME_FREEDOM}.
Respond only with valid JSON in this exact format:
{{
  "element": "{topic}",
  "time": {TIME},
  "industrial_uses": ["<use1>", "<use2>"],
  "medical_uses": ["<use1>", "<use2>"],
  "everyday_uses": ["<use1>", "<use2>"]
}}"""