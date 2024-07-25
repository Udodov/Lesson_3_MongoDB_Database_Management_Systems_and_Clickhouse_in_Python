"""
Выполним скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечём информацию о всех книгах на сайте во всех категориях: 
- id, название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание, категорию и рейтинг
Затем сохраним эту информацию в JSON-файле.
"""

import requests
from bs4 import BeautifulSoup
import json

# Базовый URL сайта
base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
book_base_url = 'http://books.toscrape.com/catalogue/'

# Функция для получения данных о книге
def get_book_data(book):
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text
    book_url = book_base_url + book.h3.a['href']
    
    # Преобразуем цену в float, удаляя символ валюты и пробелы
    price = float(price.replace('£', '').replace('Â', '').strip())
    
    # Переходим на страницу книги для извлечения описания и категории
    book_response = requests.get(book_url)
    book_soup = BeautifulSoup(book_response.text, 'html.parser')
    
    # Извлекаем количество товара в наличии
    in_stock_text = book_soup.find('p', class_='instock availability').text.strip()
    if 'In stock' in in_stock_text:
        try:
            in_stock = int(in_stock_text.split('(')[1].split()[0])
        except (IndexError, ValueError):
            in_stock = 0
    else:
        in_stock = 0
    
    # Извлекаем описание
    description_tag = book_soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'].strip() if description_tag else "No description available"
    
    # Извлекаем категорию
    category_tag = book_soup.find('ul', class_='breadcrumb').find_all('li')[2]
    category = category_tag.text.strip() if category_tag else "Unknown"

    # Извлекаем рейтинг книги
    star_rating = book.find('p', class_='star-rating')['class'][1]
    rating_map = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    rating = rating_map.get(star_rating, 0)

    return {
        'title': title,
        'price': price,
        'in_stock': in_stock,
        'description': description,
        'category': category,
        'rating': rating
    }

# Функция для получения данных со всех страниц
def scrape_all_pages():
    books_data = []
    page_number = 1

    while True:
        url = base_url.format(page_number)
        response = requests.get(url)
        response.encoding = 'utf-8'
        
        # Проверяем успешность запроса
        if response.status_code != 200:
            break

        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все элементы книги на странице
        books = soup.find_all('article', class_='product_pod')

        # Если книги не найдены, значит достигли последней страницы
        if not books:
            break

        # Извлекаем данные о книгах и добавляем их в общий список
        for book in books:
            books_data.append(get_book_data(book))

        print(f"Страница {page_number} обработана.")
        page_number += 1

    return books_data

# Скрейпим данные со всех страниц
all_books_data = scrape_all_pages()

# Сохраняем данные в JSON файл
with open('all_books_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_books_data, f, indent=4, ensure_ascii=False)

print("Данные успешно сохранены в all_books_data.json")
