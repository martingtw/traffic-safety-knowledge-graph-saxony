from rdflib import Graph, Namespace

g = Graph()
EX = Namespace("http://example.org/traffic/")
g.bind("ex", EX)
