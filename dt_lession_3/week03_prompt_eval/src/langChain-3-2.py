import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver  

load_dotenv()


# Create a Groq chat model instance
model = ChatGroq(
    model="qwen/qwen3-32b",  
    temperature=0
)

model = ChatOpenAI(
    model="mistral",
    api_key=os.environ["GPUSTACK_API_KEY"],  
    base_url="http://127.0.0.1:11434/v1", 
    temperature = 0.7,
    checkpointer=InMemorySaver()
)

# Messages
system_msg = SystemMessage("You are a helpful assistant.")
human_msg = HumanMessage("Hello, Who are you?")
ai_msg = AIMessage("")  #to give a start to the ai

messages = [system_msg, human_msg, ai_msg]

# 3.2
print("==3.2==")
# Use it to invoke a chat
response = model.invoke(messages) # Returns AIMessage
# print(response)
print(response.content)
print("\n")
print(response.response_metadata)
print("\n\n")

