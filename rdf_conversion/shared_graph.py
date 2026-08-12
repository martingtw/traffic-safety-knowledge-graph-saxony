from rdflib import Graph, Namespace

g = Graph()
EX = Namespace("http://example.org/")
g.bind("ex", EX)
