# Traffic Safety Knowledge Graph Saxony

Semantic-Web-Projekt zur Verknüpfung offener Verkehrssicherheitsdaten für Sachsen in einem RDF-Wissensgraphen. Das Projekt kombiniert Daten zu stationären Geschwindigkeitsmessstellen, Verkehrsunfällen und kommunalen Statistiken der 418 sächsischen Gemeinden, um sie über SPARQL gemeinsam auswerten zu können.


## Datenquellen
1. **OpenStreetMap** - stationäre Geschwindigkeitsmessstellen (Koordinaten, Fahrtrichtung, zulässige Höchstgeschwindigkeit)
2. **Unfallatlas** - Verkehrsunfälle mit Personenschaden aus 2025 (Unfallkategorie, Zeitpunkt, Koordinaten, beteiligte Fahrzeugarten)
3. **Statistisches Landesamt Sachsen** - Einwohnerzahlen, Pkw-Bestand und Gebietsfächen je Gemeinde

## Ablauf
Offene Datenquelle --> Python-Extraktion --> RDF/Turtle --> Fuseki-Triplestore --> SPARQL --> Auswertung

## Repository-Struktur
- `rdf_conversion/` - Python-Extraktionsskripte (Quelle 1-3 zu RDF)
- `rdf_output/` - erzeugte Turtle-Dateien der drei Quellen
- `ontology/` - Turtle-Datei zum Vokabular
- `queries/` - SPARQL-Anfragen
- `geo/` - Hilfsskript zur Gemeindezuordnung (geo_utils.py)
- `notebook/` - Jupyter Notebook zur Analyse inkl. PDF-Export
- `fuseki/` - Startskript für den Fuseki-Podman-Container
- `data/` - Rohdaten (GADM-Geodaten aus Lizenzgründen nicht enthalten)


## Setup
Die GADM-Gemeindegrenzen (`data/gadm/gadm41_DEU_4.json`) sind aus Lizenzgründen nicht im Repository enthalten. Vor dem ersten Ausführen der Extraktionsskripte selbst herunterladen und unter `data/gadm/` ablegen:

   wget https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_DEU_4.json.zip

Das Skript `main.py` startet automatisch alle Extraktionsskripte.

Fuseki läuft lokal über einen Podman-Container (`fuseki/`), Dataset-Name `traffic-safety`, Speichertyp Persistent (TDB2). Die fünf Turtle-Dateien aus `rdf_output/` und `ontology/` werden über die Fuseki-Weboberfläche ("Add data") geladen. Details siehe Kapitel 4 der Dokumentation.

## Notebook ausführen

Voraussetzungen:
- Fuseki läuft und das Dataset `traffic-safety` ist befüllt
- `pip install SPARQLWrapper pandas matplotlib jupyter --break-system-packages`

Danach im Ordner `notebook/`:
    jupyter notebook traffic_safety_analysis.ipynb

Falls die Ausführung nicht möglich ist, liegt zusätzlich ein statischer Export als
`traffic_safety_analysis.pdf` bei.

## Poster
Projektposter für den Leipziger Semantic Web Tag 2026:
[Poster](poster/lswt-2026-traffic-safety-kg-saxony-poster.pdf)