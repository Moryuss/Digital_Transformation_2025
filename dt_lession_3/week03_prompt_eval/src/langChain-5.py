import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.utilities import SQLDatabase
import db_sqlite
import sqlite3

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



system_msg = SystemMessage('''You are a helpful assistant.''')
human_msg = HumanMessage("Hello, Make an sql query and take the first element of the table: the schema is [id, page, doc_content]. The table name is docs" \
                        "The output must be a valid SQLite query, nothing more /nothink")
ai_msg = AIMessage("")  # to give a start to the ai


messages=[system_msg,human_msg]
# aggiunta docs al db

# for i, doc in enumerate(db_docs):
#     db_sqlite.add_doc_to_sqlite_db(i,doc.metadata["page"],doc.page_content)


# DB SQLite print docs
# conn = sqlite3.connect("rag.db")
# cursor = conn.cursor()

# cursor.execute("""SELECT * FROM docs""")
# rows = cursor.fetchall()

response = model.invoke(messages)

print(response.content)
db_sqlite.execute_query(response.content)

