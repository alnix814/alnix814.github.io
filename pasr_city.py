import requests
import json

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
area["name"="Россия"]->.boundary; 

// Получение городов с меткой "place=city"
node(area.boundary)["place"="city"]->.cities;

foreach.cities -> .city (
    // Выводим название города
    node.city;
    out center;

    // Получаем все улицы в каждом городе
    way(area.city)["highway"="residential"];
    out tags;   // Улицы с названиями
    
    // Получаем здания с адресными метками (номерами домов)
    node(area.city)["addr:housenumber"];
    out tags;   // Здания с номерами домов
);
"""

response = requests.get(overpass_url, params={'data': overpass_query})
data = response.json()


selected_data = []
for element in data["elements"]:
    if "tags" in element and "name" in element["tags"]:
        selected_data.append({"name": element["tags"]["name"]})

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(selected_data, f, ensure_ascii=False, indent=4)

print('все')