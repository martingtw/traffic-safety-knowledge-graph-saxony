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
    df.columns[1]: "name",
})

def make_uri(code):
    code = code.replace("/", "_")
    code = code.replace(".", "")
    code = code.replace(" ", "_")
    code = "muni_" + code
    return URIRef(EX[code])

def to_float(value):
    try:
        return float(str(value))
    except:
        return None

# Iterate through rows
for _, row in df.iterrows():
    code = str(row["code"])
    name = str(row["name"])
    area = to_float(row["qkm"])
    
    if len(code) != 8 or not code.isdigit():
        continue

    name = name.strip()
    
    # RDF Triple
    uri = make_uri(code)

    g.add((uri, RDF.type, EX.Municipality))
    g.add((uri, EX.ags, Literal(code)))
    g.add((uri, EX.name, Literal(name)))
    g.add((uri, EX.area_km2, Literal(area, datatype=XSD.decimal)))