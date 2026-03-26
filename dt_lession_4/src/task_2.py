from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

def run_sparql(query: str) -> dict:
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    result = sparql.query().convert()
    return result["results"]["bindings"]

def clean_sparql(sparql):   
    clean = [{k: v["value"] for k, v in row.items()} for row in sparql]
    return pd.DataFrame(clean)

def text_sparql(sparql: pd.DataFrame):
    company_list = sparql["itemLabel"]
    result = "The Biggest software companies (by money) are: "
    for c in company_list:
        result += c+","
    return result

query = '''
SELECT ?item ?itemLabel
WHERE {
  ?item wdt:P31 wd:Q1058914.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
  }
  LIMIT 20
  '''
result = clean_sparql(run_sparql(query))
print((result["itemLabel"].to_numpy() + result["item"].to_numpy()).tolist())

# print(text_sparql(result))


