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
    df.columns[3]: "cars_total",
    df.columns[4]: "cars_pkw"
})

def make_uri(code):
    code = code.replace("/", "_")
    code = code.replace(".", "")
    code = code.replace(" ", "_")
    code = "muni_" + code
    return URIRef(EX[code])

def to_int(value):
    try:
        return int(float(value))
    except:
        return None

# Iterate through rows
for _, row in df.iterrows():
    code = str(row["code"])
    cars_pkw = to_int(row["cars_pkw"])
    
    if len(code) != 8 or not code.isdigit():
        continue
   
    # RDF Triple
    uri = make_uri(code)

    g.add((uri, RDF.type, EX.Municipality))
    g.add((uri, EX.cars_pkw, Literal(cars_pkw, datatype=XSD.integer)))