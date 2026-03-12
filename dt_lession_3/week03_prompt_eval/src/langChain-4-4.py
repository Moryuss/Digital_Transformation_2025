import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_chroma import Chroma
from langchain_core.documents import Document

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

# document loading - automatic chunking 
docs = load_pdf(data_path)
db_docs =[]
db_ids = []
id=0

# Creazione dei documenti da mettere nel vector_db
for doc in docs:
    #  print(f"File: {doc.metadata['source']} | Pagina: {doc.metadata['page']}")
    #  print(doc.page_content[:25])
    #  print("---")
    db_docs.append(Document(
        page_content=doc.page_content,
        metadata={
            "page": doc.metadata['page'],
            "source": doc.metadata['source']
        }
        ))
    db_ids.append(str(id))
    id=id+1


# Embedding and Croma (vector database)

vector_store = Chroma(
    collection_name="RAG_vector_db",
    embedding_function=modelEmbedding,
    persist_directory=chroma_path,
)

# aggiunta docs al db
vector_store.add_documents(documents=db_docs, ids=db_ids)


system_msg = SystemMessage('''You are a helpful assistant. 
                           Answer the users QUESTION using the DOCUMENTS text given to you.
                           Keep your answer ground in the facts of the DOCUMENT.
                           If the DOCUMENT doesn't contain the facts to answer the QUESTION say <<No information regarding {argument} were found in the documents>>
                           EVEN IF you know he answer, if it is not written in the Documents then do not tell me''')
human_msg = HumanMessage("Hello, can you explain what is oassododd?")
ai_msg = AIMessage("")  # to give a start to the ai

rag_result = vector_store.similarity_search(
    human_msg.content,
    k=2
)

rag_message = ""
for i, r in enumerate(rag_result): 
    rag_message += "DOCUMENT " + str(i) + ": "  
    rag_message += r.page_content + "\n"

rag_message += "User: " + human_msg.content 
messages = [system_msg, human_msg, ai_msg]

response = model.invoke(messages)
print(response.content)

