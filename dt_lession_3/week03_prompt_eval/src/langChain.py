import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


# Create a Groq chat model instance
model = ChatGroq(
    model="qwen/qwen3-32b",  
    temperature=0
)

# Use it to invoke a chat
response = model.invoke("Hello")
print(response.content)