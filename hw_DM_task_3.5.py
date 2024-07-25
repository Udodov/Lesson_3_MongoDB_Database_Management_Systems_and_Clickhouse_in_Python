from clickhouse_driver import Client
import json

# Подключение к серверу ClickHouse
client = Client("localhost")

# Создание базы данных (если она не существует)
client.execute("CREATE DATABASE IF NOT EXISTS library")

# Создание таблицы
client.execute(
    """
CREATE TABLE IF NOT EXISTS library.books (
    id UInt64,
    title String,
    author String,
    price Float64,
    rating Int32,
    category String,
    in_stock Int32
) ENGINE = MergeTree()
ORDER BY id
"""
)

print("Таблица создана успешно.")

# Чтение данных из файла
with open("all_books_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Преобразование данных в формат, подходящий для вставки
formatted_data = [
    (
        item.get(
            "id", 0
        ),  # Пожалуйста, убедитесь, что поле 'id' существует и уникально
        item["title"],
        item.get("author", ""),  # Если нет автора, используем пустую строку
        item["price"],
        item["rating"],
        item["category"],
        item["in_stock"],
    )
    for item in data
]

# Вставка данных в таблицу
client.execute(
    "INSERT INTO library.books (id, title, author, price, rating, category, in_stock) VALUES",
    formatted_data,
)

print("Данные успешно загружены.")

# Проверка успешности вставки
result = client.execute("SELECT * FROM library.books LIMIT 1")
print("Вставленная запись:", result[0])

# Просмотр структуры таблицы
structure = client.execute("DESCRIBE TABLE library.books")
print("Структура таблицы:")
for column in structure:
    print(column)

# Просмотр первых 10 записей в таблице
data = client.execute("SELECT * FROM library.books LIMIT 10")
print("Данные в таблице:")
for row in data:
    print(row)
