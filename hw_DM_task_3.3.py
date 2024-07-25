"""
- Используем проекцию подсчета и отображения количество книг каждой из категорий.
"""

from pymongo import MongoClient
import json

# создание экземпляра клиента
client = MongoClient()

# подключение к базе данных и коллекции
db = client["books_to_scrape"]
collection = db["library"]

# Агрегационный запрос для подсчета количества книг в каждой категории
pipeline = [
    {
        "$group": {
            "_id": "$category",  # Группировка по полю "category"
            "count": {"$sum": 1},  # Подсчет количества документов в каждой группе
        }
    },
    {"$sort": {"count": -1}},  # Сортировка по количеству в порядке убывания
]

# Выполнение агрегационного запроса
category_counts = collection.aggregate(pipeline)

# Вывод результатов
for category_count in category_counts:
    print(f"Category: {category_count['_id']}, Count: {category_count['count']}")

# Получение количества документов в коллекции с помощью функции count_documents()
count = collection.count_documents({})
print(f"Число записей в базе данных: {count}")
