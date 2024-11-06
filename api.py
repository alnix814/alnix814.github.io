import json
import csv
import requests

# Подставьте ваш API-ключ от Unsplash
UNSPLASH_ACCESS_KEY = 'PJZdOy9RI4mntMf3o9wPOrD463K10KU3ox0TEWw6Kok'

# Функция для получения URL изображения
def get_image_url(query):
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    data = response.json()
    
    # Проверяем, есть ли результаты
    if data["results"]:
        # Берем URL первого изображения
        return data["results"][0]["urls"]["small"]
    else:
        return None

# Загрузка данных JSON
with open('newdata.json', 'r', encoding='utf-8') as f:
    addresses_data = json.load(f)

with open('data.json', 'r', encoding='utf-8') as f:
    cities_data = json.load(f)

# Открываем CSV файл для записи
with open('addresses_with_images.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['City', 'Street', 'House Number', 'Image URL'])
    
    # Обрабатываем каждый город из cities_data
    for i, city in enumerate(cities_data):
        city_name = city["name"]
    
        # Проверка наличия адресов для города
        if city_name in addresses_data and addresses_data[city_name]:
            for i, address in enumerate(addresses_data[city_name]):
                street = address['street']
                housenumber = address['housenumber']
                
                # Формируем запрос и получаем URL изображения
                query = f"Большой дом"
                image_url = get_image_url(query)
                
                writer.writerow([city_name, street, housenumber, image_url])

        else:
            writer.writerow([city_name, '', '', ''])

print("Данные с изображениями успешно записаны в файл addresses_with_images.csv")
