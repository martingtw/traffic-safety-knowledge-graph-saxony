import os
import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD
from rdf_conversion.shared_graph import g, EX

# Load file
BASE_DIR = os.path.dirname(__file__)
INPUT_FILE = os.path.join(BASE_DIR, "../data/source3/11111-040M.xlsx")

df = pd.read_excel(INPUT_FILE, skiprows=4)

df = df.rename(columns={
    df.columns[0]: "code",
    df.columns[1]: "municipality",
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

def to_float(value):
    try:
        return float(str(value))
    except:
        return None

# Iterate through rows
for _, row in df.iterrows():
    code = str(row["code"])
    municipality = str(row["municipality"])
    area = to_float(row["qkm"])
    
    if len(code) != 8 or not code.isdigit():
        continue

    clean = clean_name(municipality)
    results.append(clean)
    
    # RDF Triple
    uri = make_uri(clean)

    g.add((uri, RDF.type, EX.Municipality))
    g.add((uri, EX.name, Literal(clean)))
    g.add((uri, EX.area_km2, Literal(area, datatype=XSD.decimal)))