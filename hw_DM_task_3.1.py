"""
- Создадим базу данных и коллекции для их хранения в MongoDB
"""

import json
from pymongo import MongoClient

# Подключение к серверу MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Выбор базы данных и коллекции
db = client["books_to_scrape"]
collection = db["library"]

# Чтение файла JSON с указанием кодировки
with open("all_books_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Функция разделения данных на более мелкие фрагменты
def chunk_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i: i + chunk_size]

# Разделение данных на фрагменты по 1000 записей в каждом
chunk_size = 1000
data_chunks = list(chunk_data(data, chunk_size))

# Вставка фрагментов в коллекцию MongoDB
for chunk in data_chunks:
    collection.insert_many(chunk)

print("Данные успешно вставлены.")

