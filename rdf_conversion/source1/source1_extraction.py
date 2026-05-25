import json
import re
from pathlib import Path
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD

INPUT_FILE = "source_1.geojson"
OUTPUT_FILE = "source1_osm_speed_cameras.ttl"

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

    camera_uri = EX[f"speed-camera-{slugify(osm_id)}"]

    g.add((camera_uri, RDF.type, EX.SpeedCamera))
    g.add((camera_uri, RDFS.label, Literal(f"Speed camera {osm_id}", lang="en")))
    g.add((camera_uri, EX.osmId, Literal(osm_id)))
    g.add((camera_uri, EX.source, URIRef(f"https://www.openstreetmap.org/{osm_id}")))

    # Coordinates
    if geometry.get("type") == "Point":
        lon, lat = geometry["coordinates"]

        g.add((camera_uri, EX.latitude, Literal(lat, datatype=XSD.decimal)))
        g.add((camera_uri, EX.longitude, Literal(lon, datatype=XSD.decimal)))

    # OSM-Tags
    add_if_present(g, camera_uri, EX.direction, properties.get("direction"))
    
    maxspeed = parse_int(properties.get("maxspeed"))
    if maxspeed is not None:
        g.add((camera_uri, EX.hasMaxSpeed, Literal(maxspeed, datatype=XSD.integer)))

    add_if_present(g, camera_uri, EX.abandoned, properties.get("abandoned"))

g.serialize(destination=OUTPUT_FILE, format="turtle")

print(f"Converted {len(data['features'])} speed camera features to RDF.")
print(f"Saved RDF to {OUTPUT_FILE}")