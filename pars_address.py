import requests
import json
from tqdm import tqdm

with open('data.json', encoding='utf-8') as f:
    citys = json.load(f)

all_data = {}

for c in tqdm(citys, desc='Обработка информации', total=195):

    city = c.get('name', {})

    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json];
        area["name"="{city}"]["place"="city"]->.searchArea;
        (
        node["addr:street"](area.searchArea);
        way["addr:street"](area.searchArea);
        relation["addr:street"](area.searchArea);
        );
        out body;
        """

    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
 
    selected_data = []
    point = 0
    for element in data["elements"]:
        tags = element.get("tags", {})
        address = {
            "street": tags.get("addr:street"),
            "housenumber": tags.get("addr:housenumber"),
        }
        if address["street"] and address["housenumber"]:
            selected_data.append(address)
            point += 1

        if point > 10:
            break
    
    all_data[city] = selected_data

with open("newdata.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print("Адреса успешно записаны в 'newdata.json'.")