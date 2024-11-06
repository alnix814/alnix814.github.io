import json
import csv

# # Загружаем данные из файлов JSON
# with open('newdata.json', 'r', encoding='utf-8') as f:
#     addresses_data = json.load(f)

# with open('data.json', 'r', encoding='utf-8') as f:
#     cities_data = json.load(f)

# # Открываем CSV файл для записи объединенных данных
# with open('combined_addresses.csv', mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
    
#     # Записываем заголовок
#     writer.writerow(['City', 'Street', 'House Number'])
    
#     # Проходим по каждому городу в cities_data
#     for city in cities_data:
#         city_name = city["name"]
        
#         # Проверяем, есть ли адреса для данного города
#         if city_name in addresses_data and addresses_data[city_name]:
#             # Если адреса есть, записываем каждую запись адреса
#             for address in addresses_data[city_name]:
#                 writer.writerow([city_name, address['street'], address['housenumber']])
#         else:
#             # Если адресов нет, записываем город с пустыми значениями для улицы и номера дома
#             writer.writerow([city_name, '', ''])

# print("Данные успешно объединены и записаны в файл combined_addresses.csv")


column_to_delete = "Image URL"

# Читаем исходный CSV файл и удаляем указанный столбец
with open('addresses_with_images.csv', mode='r', encoding='utf-8') as infile, open('updated_addresses.csv', mode='w', newline='', encoding='utf-8') as outfile:
    # Читаем файл как словарь
    reader = csv.DictReader(infile)
    
    # Определяем имена столбцов, исключая тот, который нужно удалить
    fieldnames = [field for field in reader.fieldnames if field != column_to_delete]
    
    # Записываем результат в новый файл
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()  # записываем заголовки
    
    for row in reader:
        # Удаляем столбец из строки
        row.pop(column_to_delete, None)
        # Записываем измененную строку
        writer.writerow(row)

print("Столбец успешно удален и файл обновлен как 'updated_addresses.csv'")
