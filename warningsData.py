# warningsData.py

import requests
import json
import numpy as np
from sklearn.cluster import DBSCAN
import urllib.parse
from shapely.geometry import shape
import matplotlib.pyplot as plt

BASE_URL = "https://services9.arcgis.com/RHVPKKiFTONKtxq3/ArcGIS/rest/services/NWS_Watches_Warnings_v1/FeatureServer/"
INTERESTED_EVENTS = [
    "Flash Flood Warning", "Hydrologic Advisory", "Hydrologic Outlook",
    "Low Water Advisory", "Flash Flood Statement", "Flash Flood Watch",
    "Flood Advisory", "Flood Statement", "Flood Warning", "Flood Watch",
    "Dust Storm Warning"
]
LAYERS = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]

def encode_events(events):
    return ','.join([f"'{urllib.parse.quote(event)}'" for event in events])

def fetch_data_from_layer(layer_id, where_clause):
    query = f"query?where={where_clause}&outFields=*&returnGeometry=true&f=pgeojson"
    response = requests.get(BASE_URL + str(layer_id) + '/' + query)
    if response.status_code == 200:
        data = response.json()
        if 'features' in data:
            return data['features']
        else:
            return []
    else:
        print(f"Failed to fetch data from layer {layer_id}. Status code: {response.status_code}, Response: {response.text}")
        return []

def process_layers(layers, where_clause):
    coordinates = []
    event_properties = {}
    layer_summary = {}

    for layer in layers:
        features = fetch_data_from_layer(layer, where_clause)
        print(f"Layer {layer}: Found {len(features)} features")

        layer_summary[layer] = {
            "total_features": len(features),
            "valid_coordinates": 0,
            "invalid_geometries": 0
        }

        for feature in features:
            if 'geometry' in feature:
                geom_type = feature['geometry']['type']
                geom = shape(feature['geometry'])

                if geom_type == 'Point':
                    lat = feature['geometry']['coordinates'][1]
                    lon = feature['geometry']['coordinates'][0]
                    coordinates.append([lat, lon])

                    event_type = feature['properties']['Event']
                    if event_type not in event_properties:
                        event_properties[event_type] = []
                    event_properties[event_type].append({
                        "layer_id": layer,
                        "latitude": lat,
                        "longitude": lon,
                        "properties": feature['properties']
                    })
                    layer_summary[layer]["valid_coordinates"] += 1

                elif geom_type in ['Polygon', 'MultiPolygon']:
                    centroid = geom.centroid
                    coordinates.append([centroid.y, centroid.x])

                    event_type = feature['properties']['Event']
                    if event_type not in event_properties:
                        event_properties[event_type] = []
                    event_properties[event_type].append({
                        "layer_id": layer,
                        "latitude": centroid.y,
                        "longitude": centroid.x,
                        "properties": feature['properties']
                    })
                    layer_summary[layer]["valid_coordinates"] += 1

                else:
                    layer_summary[layer]["invalid_geometries"] += 1
            else:
                layer_summary[layer]["invalid_geometries"] += 1

    return coordinates, event_properties, layer_summary

def apply_dbscan(coordinates, eps=0.1, min_samples=3):
    if len(coordinates) > 0:
        coords = np.array(coordinates)
        db = DBSCAN(eps=eps, min_samples=min_samples).fit(coords)
        labels = db.labels_

        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)

        print(f"Number of clusters found by DBSCAN: {n_clusters}")
        print(f"Number of noise points found by DBSCAN: {n_noise}")

        return labels, n_clusters, n_noise
    else:
        print("No valid coordinates found for DBSCAN clustering.")
        return [], 0, 0

def main():
    encoded_event_names = encode_events(INTERESTED_EVENTS)
    where_clause = f"Event IN ({encoded_event_names})"
    
    coordinates, event_properties, layer_summary = process_layers(LAYERS, where_clause)
    
    labels, n_clusters, n_noise = apply_dbscan(coordinates)

    for idx, label in enumerate(labels):
        if label == -1:
            continue
        for event_type, properties in event_properties.items():
            if properties[idx]['latitude'] == coordinates[idx][0] and properties[idx]['longitude'] == coordinates[idx][1]:
                properties[idx]['cluster_id'] = label

    return event_properties, coordinates, labels

if __name__ == "__main__":
    main()
