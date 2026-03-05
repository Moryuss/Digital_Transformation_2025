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
    temperature = 0.2,
)

# Messages (history)

system_msg = SystemMessage("You are a helpful assistant.")

# where i will save the history of the conversation
history = [system_msg]
turns = ["Hello, what's your name?",
        "I am Matteo, you have a nice name, what is it's origin",
         "when were you created?",
         "What's my name?"]

# messages = [system_msg, human_msg, ai_msg]

#3.3
print("==3.3==") # memory bw/ messages
print("system msg:", system_msg)
for i, msg in enumerate(turns, start=1):
    history.append(HumanMessage(content=msg)) # mio messaggio
    response = model.invoke(history)    # invii system prompt + messaggio
    history.append(AIMessage(content=response.content)) # salvi messaggio dell'AI
    print(f'Turn {i}')
    print('User:', msg)
    print('AI:', response.content)
    print()