import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD

INPUT_FILE = "csv/Unfallorte2024_LinRef.csv"
OUTPUT_FILE = "source2_saxony_accidents.ttl"

EX = Namespace("http://example.org/traffic/")

def parse_decimal(value):
    if pd.isna(value):
        return None
    return float(str(value).replace(",", ".").strip())

def parse_int(value):
    if pd.isna(value):
        return None
    try:
        return int(str(value).strip())
    except ValueError:
        return None

def add_if_present(graph, subject, predicate, value, datatype=None):
    if value is not None and not pd.isna(value) and str(value).strip() != "":
        if datatype:
            graph.add((subject, predicate, Literal(value, datatype=datatype)))
        else:
            graph.add((subject, predicate, Literal(str(value))))

df = pd.read_csv(INPUT_FILE, sep=";", encoding="utf-8-sig", dtype=str)
saxony = df[df["ULAND"].str.zfill(2) == "14"].copy() # filter saxony (ULAND = 14)

print("Loaded", len(df), "accident records.")
print("Filtered", len(saxony), "accident records for Saxony.")

g = Graph()
g.bind("ex", EX)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)

g.add((EX.saxony, RDF.type, EX.FederalState))
g.add((EX.saxony, RDFS.label, Literal("Sachsen", lang="de")))

for _, row in saxony.iterrows():
    accident_id = row["UIDENTSTLAE"]
    accident_uri = EX[f"accident-{accident_id}"]

    g.add((accident_uri, RDF.type, EX.TrafficAccident))
    g.add((accident_uri, RDFS.label, Literal(f"Traffic accident {accident_id}", lang="en")))
    g.add((accident_uri, EX.locatedIn, EX.saxony))
    g.add((accident_uri, EX.source, URIRef("https://unfallatlas.statistikportal.de/")))

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

g.serialize(destination=OUTPUT_FILE, format="turtle")

print("Saved RDF to", OUTPUT_FILE)