import requests
from bs4 import BeautifulSoup
import csv


def get_books_urls_by_category(category_name, category_id) -> list[str]:
    url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/index.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    book_urls = []

    for book in soup.find_all("article", class_="product_pod"):
        link = book.find("a")
        book_url = link.get("href")
        absolute_book_url = f"https://books.toscrape.com/catalogue/{book_url}"
        book_urls.append(absolute_book_url)

    with open("book_category_urls.csv", "w") as f:
        for url in book_urls:
            f.write(f"{url}\n")

    return book_urls


travel_book_urls = get_books_urls_by_category("travel", "2")
print(travel_book_urls)


# def get_books_by_category():
#    get_book


#     return fiction_books


# fiction_books = get_books_by_category()
# print(fiction_books)
