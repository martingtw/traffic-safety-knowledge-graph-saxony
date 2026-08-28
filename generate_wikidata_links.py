# pip install SPARQLWrapper rdflib --break-system-packages
# Erstellt mit Unterstützung von Claude (Anthropic), anschließend manuell 
# geprüft und gegen Wikidata-Endpunkt getestet
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Namespace, URIRef, OWL
import re

EX = Namespace("http://example.org/traffic/")
WD = Namespace("http://www.wikidata.org/entity/")

own_ags = set()
with open("rdf_output/source3_saxony_municipal_stats.ttl", encoding="utf-8") as f:
    content = f.read()
    own_ags = set(re.findall(r'ex:ags\s+"(\d{8})"', content))

print(f"Found {len(own_ags)} own AGS values")

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""
    SELECT ?item ?ags WHERE {
      ?item wdt:P439 ?ags .
      FILTER(STRSTARTS(?ags, "14"))
    }
""")
sparql.setReturnFormat(JSON)
sparql.agent = "TrafficSafetyKG-Sachsen/1.0 (Uniprojekt Semantic Web)"
results = sparql.query().convert()

wikidata_map = {}
for row in results["results"]["bindings"]:
    ags = row["ags"]["value"]
    qid = row["item"]["value"].split("/")[-1]
    wikidata_map[ags] = qid

print(f"Found {len(wikidata_map)} municipalities with AGS at Wikidata")

g = Graph()
g.bind("ex", EX)
g.bind("wd", WD)
g.bind("owl", OWL)

matched, unmatched = 0, []
for ags in own_ags:
    if ags in wikidata_map:
        subj = EX[f"muni_{ags}"]
        obj = WD[wikidata_map[ags]]
        g.add((subj, OWL.sameAs, obj))
        matched += 1
    else:
        unmatched.append(ags)

print(f"{matched} of {len(own_ags)} municipalities successfully linked")
if unmatched:
    print("Not found:", unmatched)

g.serialize(destination="rdf_output/links_wikidata.ttl", format="turtle")
print("Saved: links_wikidata.ttl")
