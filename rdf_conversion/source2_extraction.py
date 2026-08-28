import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
import os
from geo.geo_utils import get_municipality

BASE_DIR = os.path.dirname(__file__)
INPUT_FILE = os.path.join(BASE_DIR, "../data/source2/Unfallorte_2025_LR_BasisDLM.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "../rdf_output/source2_saxony_accidents.ttl")

EX = Namespace("http://example.org/traffic/")

def parse_decimal(value):
    return float(str(value).replace(",", ".").strip())

def parse_int(value):
    return int(str(value).strip())

def add_if_present(graph, subject, predicate, value, datatype=None):
    if value is not None and not pd.isna(value) and str(value).strip() != "":
        if datatype:
            graph.add((subject, predicate, Literal(value, datatype=datatype)))
        else:
            graph.add((subject, predicate, Literal(str(value))))

def make_uri(ags):
    return URIRef(EX[f"muni_{ags}"])

df = pd.read_csv(INPUT_FILE, sep=";", encoding="utf-8-sig", dtype=str)
saxony = df[df["ULAND"].str.zfill(2) == "14"].copy() # filter saxony (ULAND = 14)

g = Graph()
g.bind("ex", EX)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)

for _, row in saxony.iterrows():
    accident_id = row["UIDENTSTLAE"]
    accident_uri = EX[f"accident_{accident_id}"]

    g.add((accident_uri, RDF.type, EX.TrafficAccident))
    g.add((accident_uri, RDFS.label, Literal(f"Traffic accident {accident_id}", lang="en")))
    
    year = parse_int(row["UJAHR"])
    month = parse_int(row["UMONAT"])
  
    if year is not None:
        g.add((accident_uri, EX.accidentYear, Literal(year, datatype=XSD.gYear)))

    if month is not None:
        g.add((accident_uri, EX.accidentMonth, Literal(month, datatype=XSD.integer)))

    add_if_present(g, accident_uri, EX.accidentCategoryCode, row["UKATEGORIE"])
    add_if_present(g, accident_uri, EX.involvesCar, row["IstPKW"], XSD.integer)
    add_if_present(g, accident_uri, EX.involvesMotorcycle, row["IstKrad"], XSD.integer)

    # Coordinates
    lon = parse_decimal(row["XGCSWGS84"])
    lat = parse_decimal(row["YGCSWGS84"])

    if lon is not None and lat is not None:
        g.add((accident_uri, EX.longitude, Literal(lon, datatype=XSD.decimal)))
        g.add((accident_uri, EX.latitude, Literal(lat, datatype=XSD.decimal)))

        ags = get_municipality(lat, lon)

        if ags:
            g.add((accident_uri, EX.locatedInMunicipality, make_uri(ags)))

# Explanation accidentCategoryCode
g.add((EX.accidentCategoryCode, RDF.type, RDF.Property))
g.add((EX.accidentCategoryCode, RDFS.comment, Literal("1 = Unfall mit Getöteten, 2 = Unfall mit Schwerverletzten, 3 = Unfall mit Leichtverletzten", lang="de")))

# Source description
g.add((EX.Source2Dataset, RDF.type, EX.Dataset))
g.add((EX.Source2Dataset, RDFS.label, Literal("Unfallatlas Sachsen 2025", lang="de")))
g.add((EX.Source2Dataset, EX.source, URIRef("https://unfallatlas.statistikportal.de/")))
g.add((EX.Source2Dataset, EX.retrievedOn, Literal("2026-08-17", datatype=XSD.date)))

g.serialize(destination=OUTPUT_FILE, format="turtle")

print("Source 2: Saved RDF to", OUTPUT_FILE, "\n")
