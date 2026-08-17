from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD

g = Graph()
EX = Namespace("http://example.org/traffic/")
g.bind("ex", EX)

# Source description
g.add((EX.PopulationDataset, RDF.type, EX.Dataset))
g.add((EX.PopulationDataset, EX.source, URIRef("https://www.statistik.sachsen.de/download/aktuelle-zahlen/statistik-sachsen_aI1_einwohnerzahlen-monat.xlsx")))
g.add((EX.PopulationDataset, EX.asOf, Literal("2026-04-30", datatype=XSD.date)))

g.add((EX.VehicleStockDataset, RDF.type, EX.Dataset))
g.add((EX.VehicleStockDataset, EX.source, URIRef("https://www.statistik.sachsen.de/genonline//online?operation=table&code=46251-001Z&bypass=true&levelindex=0&levelid=1786978673348")))
g.add((EX.VehicleStockDataset, EX.asOf, Literal("2025-01-01", datatype=XSD.date)))

g.add((EX.AreaDataset, RDF.type, EX.Dataset))
g.add((EX.AreaDataset, EX.source, URIRef("https://www.statistik.sachsen.de/genonline//online?operation=table&code=11111-040M&bypass=true&levelindex=1&levelid=1786567462436")))
g.add((EX.AreaDataset, EX.asOf, Literal("2024-12-31", datatype=XSD.date)))
