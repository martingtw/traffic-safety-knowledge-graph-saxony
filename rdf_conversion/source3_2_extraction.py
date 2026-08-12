import os
import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD
from rdf_conversion.shared_graph import g, EX

# Load file
BASE_DIR = os.path.dirname(__file__)
INPUT_FILE = os.path.join(BASE_DIR, "../data/source3/46251-001Z.xlsx")
OUTPUT_FILE = os.path.join(BASE_DIR, "../rdf_output/source3/source3_vehicle_stock.ttl")

df = pd.read_excel(INPUT_FILE, skiprows=5)

df = df.rename(columns={
    df.columns[0]: "code",
    df.columns[1]: "municipality",
    df.columns[3]: "cars_total",
    df.columns[4]: "cars_pkw"
})

results = []

def clean_name(name):
    name = str(name)
    name = name.split(",")[0].strip()
    return name

def make_uri(name):
    name = name.replace("/", "_")
    name = name.replace(".", "")
    name = name.replace(" ", "_")
    return URIRef(EX[name])

def to_int(value):
    try:
        return int(float(value))
    except:
        return None

# Iterate through rows
for _, row in df.iterrows():
    code = str(row["code"])
    municipality = str(row["municipality"])
    cars_pkw = to_int(row["cars_pkw"])
    
    if len(code) != 8 or not code.isdigit():
        continue

    clean = clean_name(municipality)
    results.append(clean)
    
    # RDF Triple
    uri = make_uri(clean)

    g.add((uri, RDF.type, EX.Municipality))
    g.add((uri, EX.name, Literal(clean)))
    g.add((uri, EX.cars_pkw_2025, Literal(cars_pkw, datatype=XSD.integer)))