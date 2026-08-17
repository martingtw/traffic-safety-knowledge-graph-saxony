import os
import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD
from rdf_conversion.shared_graph import g, EX

# Load file
BASE_DIR = os.path.dirname(__file__)
INPUT_FILE = os.path.join(BASE_DIR, "../data/source3/statistik-sachsen_aI1_einwohnerzahlen-monat.xlsx")
OUTPUT_FILE = os.path.join(BASE_DIR, "../rdf_output/source3/source3_saxony_residents.ttl")

df = pd.read_excel(INPUT_FILE, skiprows=5)
df.columns = df.columns.str.replace("\n", " ").str.strip()

df = df.rename(columns={
    df.columns[0]: "code",
    df.columns[1]: "name",
    df.columns[6]: "population"
})

def make_uri(code):
    code = code.replace("/", "_")
    code = code.replace(".", "")
    code = code.replace(" ", "_")
    code = "muni_" + code
    return URIRef(EX[code])

# Iterate through rows
for _, row in df.iterrows():
    code = str(row["code"])
    name = str(row["name"])
    population = row["population"]
    
    code_clean = code.replace(" ", "")

    if not code_clean.isdigit():
        continue

    if len(code_clean) != 8:
        if len(code_clean) == 5:  # Check Kreisfreie Städte
            if ", Stadt" not in name:
                continue
            code_clean = code_clean + "000"
        else:
            continue
  
    # RDF Triple
    uri = make_uri(code_clean)

    g.add((uri, RDF.type, EX.Municipality))
    g.add((uri, EX.population, Literal(population, datatype=XSD.integer)))
