# Traffic Safety Knowledge Graph Saxony

This repository contains a Semantic Web project for integrating open traffic safety data about Saxony into an RDF knowledge graph.

The project combines data about fixed speed cameras, traffic accidents and regional statistics. The goal is to make these heterogeneous datasets easier to connect, query and explore using RDF and SPARQL.

## Project status

This project is currently work in progress. The data model, queries and visualizations may change during development.

## Data sources

Planned and partially implemented sources:

1. **OpenStreetMap**
   - fixed speed camera locations in Saxony
   - coordinates, direction and speed limit where available

2. **Unfallatlas**
   - traffic accidents with personal injury
   - accident category, year and coordinates

3. **Regional statistics**
   - municipalities in Saxony
   - population and area data

## Workflow

The basic workflow is:

Open data source
→ Python extraction
→ RDF/Turtle conversion
→ Triple store
→ SPARQL queries
→ visualization
