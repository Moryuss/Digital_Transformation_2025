import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_chroma import Chroma


load_dotenv()

def load_pdf(pdf_path):
    if os.path.isdir(pdf_path):
        loader = DirectoryLoader(pdf_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    else:
        loader = PyPDFLoader(pdf_path)
    
    return loader.load()



# paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, "data")
chroma_path = os.path.join(base_dir, "chroma")


# Create a Groq chat model instance
# model = ChatGroq(
#     model="qwen/qwen3-32b",  
#     temperature=0
# )

model = ChatOpenAI(
    model="qwen3",
    api_key=os.environ["GPUSTACK_API_KEY"],  
    base_url="https://gpustack.ing.unibs.it/v1",
    temperature = 0.2,
)
modelEmbedding = OpenAIEmbeddings(
    model="qwen3-embedding",
    api_key=os.environ["GPUSTACK_API_KEY"],  
    base_url="https://gpustack.ing.unibs.it/v1"
)

# Messages (history)

system_msg = SystemMessage("You are a helpful assistant.")
human_msg = HumanMessage("Hello, Who are you?")

messages = [system_msg, human_msg]

# document loading
docs = load_pdf(data_path)

for doc in docs:
    print(f"File: {doc.metadata['source']} | Pagina: {doc.metadata['page']}")
    print(doc.page_content[:200])
    print("---")


# Embedding and Croma (vector database)

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=modelEmbedding,
    persist_directory=chroma_path,
)