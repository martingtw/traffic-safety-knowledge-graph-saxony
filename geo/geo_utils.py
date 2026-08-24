# Point-in-Polygon-Logik zur Gemeindezuordnung mit Unterstützung von ChatGPT
# (OpenAI) erstellt, anschließend manuell geprüft und angepasst.
import geopandas as gpd
from shapely.geometry import Point
import os 

# Load municipalities
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "../data/gadm/gadm41_DEU_4.json")

municipalities = gpd.read_file(DATA_PATH)
municipalities = municipalities.to_crs("EPSG:4326")

# Core function
def get_municipality(lat, lon):
    point = Point(lon, lat)
    match = municipalities[municipalities.contains(point)]

    if match.empty:
        return None

    cc4 = str(match.iloc[0]["CC_4"])
    ags = cc4[:5] + cc4[-3:]
    return ags

# Tests
# print(get_municipality(51.3397, 12.3731))
# print(get_municipality(51.204858, 12.387373))
# print(get_municipality(51.215048, 12.335929))
# print(get_municipality(51.241017, 12.382224))
# print(get_municipality(51.24945, 12.381043))
# print(get_municipality(51.269050, 12.337527))
# print(get_municipality(51.519164, 11.597279))
# print(get_municipality(51.306956, 12.375438))
# print(get_municipality(50.749148, 13.140965))
# print(get_municipality(50.484138, 12.761706))
# print(get_municipality(51.477911, 14.610763))
# print(get_municipality(50.439238, 12.942456))