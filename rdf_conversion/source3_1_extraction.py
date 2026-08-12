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

results = []

def clean_name(name):
    name = str(name)
    name = name.replace(", Stadt", "").strip()
    name = name.split(",")[0].strip()
    return name

def make_uri(name):
    name = name.replace("/", "_")
    name = name.replace(".", "")
    name = name.replace(" ", "_")
    return URIRef(EX[name])

# Iterate through rows
for _, row in df.iterrows():
    code = str(row["Schlüssel- nummer"])
    name = str(row["Land Kreisfreie Stadt Landkreis Gemeinde"])
    population = row["31. Dezember 2025"]
    
    if not code.isdigit():
        continue

    code_clean = code.replace(" ", "")

    # Kreisfreie Städte
    if len(code_clean) == 5:
        if ", Stadt" not in name:
            continue

    # Gemeinden
    elif len(code_clean) != 8:
        continue

    clean = clean_name(name)
    results.append(clean)
    
    # RDF Triple
    uri = make_uri(clean)

    g.add((uri, RDF.type, EX.Municipality))
    g.add((uri, EX.name, Literal(clean)))
    g.add((uri, EX.population_2025, Literal(population, datatype=XSD.integer)))