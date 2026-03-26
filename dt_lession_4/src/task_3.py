from SPARQLWrapper import SPARQLWrapper, JSON
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, SystemMessage


load_dotenv()

import pandas as pd
def generate_sparql(question: str) -> str:
    '''
    Given a query on a topic, the llm has to genrate a SPARQL query on it. Note that is better to specify the returned data
    Like giving a schema to parse better the answer from the panda dataframe
    '''

    model = ChatOpenAI(
        model="qwen3:30b",
        api_key="ollama",  
        base_url="http://127.0.0.1:11434/v1",
        temperature = 0.2,
    )
    system_msg = SystemMessage('''You are a helpful assistant. 
                               U have to write as answer a SPARQL query on the topic of the User, 
                               with the schema given to you by the User. 
                               The param for getting a Software Company is: ?item wdt:P31 wd:Q1058914. For the profit is wdt:P2295.
                               Do not write anything else''')
    human_msg = HumanMessage(question)

    messages = [system_msg, human_msg]
    response = model.invoke(messages)

    return response.content


def generate_final_answer(question: str) -> str:
    
    model = ChatOpenAI(
        model="qwen3:30b",
        api_key="ollama",  
        base_url="http://127.0.0.1:11434/v1",
        temperature = 0.2,
    )
    system_msg = SystemMessage('''You are a helpful assistant. 
                                use the information at given to you by the context to answer the User
                               ''')
    human_msg = HumanMessage(question)

    messages = [system_msg, human_msg]
    response = model.invoke(messages)

    return response.content


def run_wikidata_query(query: str) ->  pd.DataFrame:
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()
    result = result["results"]["bindings"]
    clean = [{k: v["value"] for k, v in row.items()} for row in result]
    return pd.DataFrame(clean)
    

def result_to_text(sparql: pd.DataFrame):
    label_col = "itemLabel" if "itemLabel" in sparql.columns else sparql.columns[0]
    companies = ", ".join(sparql[label_col].tolist())  
    return f"The biggest software companies (by gains) are: {companies}"



def answer_with_context(question: str, context: str)->str:
    response = f"History: {question}\n"           
    response += f"Context: {context}\n"           
    response += "Use the 'Context' as the only source of truth." 
    return generate_final_answer(response)


human_prompt = "Hello. I want to know about the top 20 software companies in the world by gains. I want the schema to be [itemLabel].  \nothink"
print("start")
query = generate_sparql(human_prompt)
print(f'query from LLM: {query}')

response_dict = run_wikidata_query(query=query)
print(f'wikidata answer to query: {response_dict.to_string()}')

text = result_to_text(response_dict)
print(f"result in a text readable:{text}")

answer = answer_with_context(question=query, context=text)
print(f"Final answer:%n {answer}")