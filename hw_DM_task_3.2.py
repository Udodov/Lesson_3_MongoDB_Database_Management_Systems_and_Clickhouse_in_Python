"""
- Найдем первый документ в коллекции и распечатаем его в формате JSON.
- Используем функцию count_documents(), чтобы получить общее количество документов в коллекции.
"""

from pymongo import MongoClient
import json

# создание экземпляра клиента
client = MongoClient()

# подключение к базе данных и коллекции
db = client["books_to_scrape"]
collection = db["library"]

# вывод первой записи в коллекции
all_docs = collection.find()
first_doc = all_docs[0]

# Вывод объекта JSON
pretty_json = json.dumps(first_doc, indent=4, default=str)
print(pretty_json)

# Получение количества документов в коллекции с помощью функции count_documents()
count = collection.count_documents({})
print(f'Число записей в базе данных: {count}')
