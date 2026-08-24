**Query 1 - Unfälle/1000 Einwohner/Gemeinde:**

PREFIX ex: <http://example.org/traffic/>
SELECT ?name (COUNT(?a) AS ?unfaelle) ?population
       ((COUNT(?a) * 1000.0) / ?population AS ?rate)
WHERE {
  ?a a ex:TrafficAccident ; ex:locatedInMunicipality ?m .
  ?m ex:name ?name ; ex:population ?population .
}
GROUP BY ?name ?population
ORDER BY DESC(?rate)
LIMIT 20


**Query 2 - Unfälle in jedem Monat 2025:**

PREFIX ex: <http://example.org/traffic/>
SELECT ?accidentMonth (COUNT(?a) AS ?anzahl)
WHERE { ?a a ex:TrafficAccident ; ex:accidentMonth ?accidentMonth . }
GROUP BY ?accidentMonth
ORDER BY ?accidentMonth


**Query 3 - Verteilung der Unfallschwere:**

PREFIX ex: <http://example.org/traffic/>
SELECT ?accidentCategoryCode (COUNT(?a) AS ?anzahl)
WHERE { ?a a ex:TrafficAccident ; ex:accidentCategoryCode ?accidentCategoryCode . }
GROUP BY ?accidentCategoryCode


**Query 4 - Fahrzeugdichte vs Unfallzahl:**

PREFIX ex: <http://example.org/traffic/>
SELECT ?name ?cars_pkw (COUNT(?a) AS ?unfaelle)
WHERE {
  ?m a ex:Municipality ; ex:name ?name ; ex:cars_pkw ?cars_pkw .
  ?a a ex:TrafficAccident ; ex:locatedInMunicipality ?m .
}
GROUP BY ?name ?cars_pkw


**Query 5 - Blitzerdichte je Gemeindefläche:**

PREFIX ex: <http://example.org/traffic/>
SELECT ?name ?area_km2 (COUNT(?c) AS ?blitzer)
WHERE {
  ?m a ex:Municipality ; ex:name ?name ; ex:area_km2 ?area_km2 .
  ?c a ex:SpeedCamera ; ex:locatedInMunicipality ?m .
}
GROUP BY ?name ?area_km2


**Query 6 - Geoverteilung der Unfallschwere:**

PREFIX ex: <http://example.org/traffic/>
SELECT ?latitude ?longitude ?accidentCategoryCode
WHERE { ?a a ex:TrafficAccident ; ex:latitude ?latitude ; ex:longitude ?longitude ; ex:accidentCategoryCode ?accidentCategoryCode . }


**Query 7 - Vergleich Motorrad vs PKW-Beteiligung an Unfällen nach Unfallschwere:**

PREFIX ex: <http://example.org/traffic/>
SELECT ?accidentCategoryCode 
       (SUM(?involvesCar) AS ?pkw) (SUM(?involvesMotorcycle) AS ?motorrad)
WHERE { ?a a ex:TrafficAccident ; ex:accidentCategoryCode ?accidentCategoryCode ; 
           ex:involvesCar ?involvesCar ; ex:involvesMotorcycle ?involvesMotorcycle . }
GROUP BY ?accidentCategoryCode
