# Find all software companies (instanceof sw companies)

SELECT ?item ?itemLabel
WHERE {
  ?item wdt:P31 wd:Q1058914.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
  }


# logo image optional

SELECT ?item ?itemLabel ?logo ?rank
WHERE {
  ?item wdt:P31 wd:Q1058914.
  OPTIONAL{?item wdt:P154 ?logo.}
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
  }

# fiter on revenue (money)
SELECT ?item ?itemLabel ?logo ?revenue
WHERE {
  ?item wdt:P31 wd:Q1058914.
  ?item wdt:P2139 ?revenue.
  OPTIONAL{?item wdt:P154 ?logo.}
  FILTER(?revenue >= 100000)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
  }

# lIMIT 10 E ORDERE BY REVENUE DESCENDENTE
SELECT ?item ?itemLabel ?logo ?revenue
WHERE {
  ?item wdt:P31 wd:Q1058914.
  ?item wdt:P2139 ?revenue.
  OPTIONAL{?item wdt:P154 ?logo.}
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
  }
ORDER BY DESC(?revenue) 
LIMIT 10