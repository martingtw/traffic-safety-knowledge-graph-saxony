import json
import re
from pathlib import Path
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
import os
from geo.geo_utils import get_municipality

BASE_DIR = os.path.dirname(__file__)
INPUT_FILE = os.path.join(BASE_DIR, "../data/source1/source_1.geojson")
OUTPUT_FILE = os.path.join(BASE_DIR, "../rdf_output/source1_osm_speed_cameras.ttl")

EX = Namespace("http://example.org/traffic/")
OSM = Namespace("https://www.openstreetmap.org/")

def slugify(text: str) -> str:
    text = str(text).lower()
    text = text.replace("/", "_")
    text = re.sub(r"[^a-z0-9_]+", "-", text)
    return text.strip("-")

def add_if_present(graph: Graph, subject, predicate, value, datatype=None):
    if value is not None and str(value).strip() != "":
        if datatype:
            graph.add((subject, predicate, Literal(value, datatype=datatype)))
        else:
            graph.add((subject, predicate, Literal(str(value))))

def parse_int(value):
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return None

def make_uri(ags):
    return URIRef(EX[f"muni_{ags}"])

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

g = Graph()

g.bind("ex", EX)
g.bind("osm", OSM)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)

for feature in data["features"]:
    properties = feature.get("properties", {})
    geometry = feature.get("geometry", {})

    osm_id = properties.get("@id") or feature.get("id")
    if not osm_id:
        continue

    camera_uri = EX[f"speedCamera_{osm_id.split('/')[-1]}"]

    g.add((camera_uri, RDF.type, EX.SpeedCamera))
    g.add((camera_uri, RDFS.label, Literal(f"Speed camera {osm_id}", lang="en")))
    g.add((camera_uri, EX.source, URIRef(f"https://www.openstreetmap.org/{osm_id}")))

    # Coordinates
    if geometry.get("type") == "Point":
        lon, lat = geometry["coordinates"]

        g.add((camera_uri, EX.latitude, Literal(lat, datatype=XSD.decimal)))
        g.add((camera_uri, EX.longitude, Literal(lon, datatype=XSD.decimal)))

        ags = get_municipality(lat, lon)

        if ags:
            g.add((camera_uri, EX.locatedInMunicipality, make_uri(ags)))

    # OSM-Tags
    add_if_present(g, camera_uri, EX.direction, properties.get("direction"))
    
    maxspeed = parse_int(properties.get("maxspeed"))
    if maxspeed is not None:
        g.add((camera_uri, EX.hasMaxSpeed, Literal(maxspeed, datatype=XSD.integer)))

    add_if_present(g, camera_uri, EX.abandoned, properties.get("abandoned"))

# Source description
g.add((EX.Source1Dataset, RDF.type, EX.Dataset))
g.add((EX.Source1Dataset, RDFS.label, Literal("OpenStreetMap Speed Cameras Sachsen", lang="de")))
g.add((EX.Source1Dataset, EX.source, URIRef("https://www.openstreetmap.org/")))
g.add((EX.Source1Dataset, EX.retrievedOn, Literal("2026-05-21", datatype=XSD.date)))

g.serialize(destination=OUTPUT_FILE, format="turtle")

print(f"Source 1: Saved RDF to {OUTPUT_FILE}\n")
