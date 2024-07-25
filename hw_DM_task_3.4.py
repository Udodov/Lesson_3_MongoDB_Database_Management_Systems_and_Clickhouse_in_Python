"""
- Отфильтруем документы по критерию "rating", равному "5", и подсчитаем количество совпадающих документов
- Сделаем проекцию для отображения количества книг каждой из категорий “Default” и “Nonfiction” для документов, удовлетворяющих условию, что "rating", равен "5"
- Используем операторы $lt и $gte для подсчета количества документов с "price" меньше 30 и больше или равно 30, соответственно.
- Используем оператор $regex для подсчета количества документов, содержащих слово "book" в поле "description", игнорируя регистр.
- Подсчитаем количество документов, у которых "in_stock" не равно 20 или 19.

"""

from pymongo import MongoClient

# Создание экземпляра клиента
client = MongoClient()

# Подключение к базе данных и коллекции
db = client["books_to_scrape"]
collection = db["library"]

# Определение фильтра для документов с рейтингом 5
filter_criteria = {"rating": 5}

# Подсчет количества документов, соответствующих фильтру
count = collection.count_documents(filter_criteria)
print(f"Количество документов с рейтингом 5: {count}")

if count > 0:
    # Агрегация для подсчета количества книг в категориях "Default" и "Nonfiction"
    pipeline = [
        {"$match": filter_criteria},
        {
            "$group": {
                "_id": None,
                "DefaultCount": {
                    "$sum": {"$cond": [{"$eq": ["$category", "Default"]}, 1, 0]}
                },
                "NonfictionCount": {
                    "$sum": {"$cond": [{"$eq": ["$category", "Nonfiction"]}, 1, 0]}
                },
            }
        },
        {"$project": {"_id": 0, "DefaultCount": 1, "NonfictionCount": 1}},
    ]

    # Выполнение агрегации
    result = list(collection.aggregate(pipeline))

    # Вывод результата агрегации
    if result:
        print(f'Количество книг в категории Default: {result[0]["DefaultCount"]}')
        print(f'Количество книг в категории Nonfiction: {result[0]["NonfictionCount"]}')
else:
    print("Нет документов с рейтингом 5.")

# Подсчет количества документов с "price" меньше 30
price_less_than_30_count = collection.count_documents({"price": {"$lt": 30}})
print(f"Количество документов с ценой меньше 30: {price_less_than_30_count}")

# Подсчет количества документов с "price" больше или равно 30
price_gte_30_count = collection.count_documents({"price": {"$gte": 30}})
print(f"Количество документов с ценой больше или равно 30: {price_gte_30_count}")

# Подсчет количества документов, содержащих слово "book" в поле "description", игнорируя регистр
description_contains_book_count = collection.count_documents({"description": {"$regex": "book", "$options": "i"}})
print(f"Количество документов с описанием, содержащим слово 'book': {description_contains_book_count}")

# Подсчет количества документов, у которых "in_stock" не равно 20 или 19
in_stock_not_20_or_19_count = collection.count_documents({"in_stock": {"$nin": [19, 20]}})
print(f"Количество документов, у которых 'in_stock' не равно 20 или 19: {in_stock_not_20_or_19_count}")

