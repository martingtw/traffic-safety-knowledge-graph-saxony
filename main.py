from rdf_conversion.shared_graph import g

import rdf_conversion.source1_extraction as s1
import rdf_conversion.source2_extraction as s2
import rdf_conversion.source3_1_extraction as s31
import rdf_conversion.source3_2_extraction as s32
import rdf_conversion.source3_3_extraction as s33

OUTPUT_FILE = "rdf_output/source3_saxony_municipal_stats.ttl" 
g.serialize(OUTPUT_FILE, format="turtle")
print(f"Source 3: Saved RDF to {OUTPUT_FILE}")