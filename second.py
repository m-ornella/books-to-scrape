import requests
from bs4 import BeautifulSoup
import csv

from first import get_book


# loop through all book urls in travel category
def get_books_urls_by_category(category_name, category_id) -> list[str]:
    url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/index.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    book_urls = []

    for book in soup.find_all("article", class_="product_pod"):
        link = book.find("a")
        book_url = link.get("href")
        absolute_book_url = f"https://books.toscrape.com/catalogue/{book_url[9:]}"
        book_urls.append(absolute_book_url)

    # with open("book_category_urls.csv", "w") as f:
    #     for url in book_urls:
    #         f.write(f"{url}\n")

    return book_urls


# travel_book_urls = get_books_urls_by_category("travel", "2")
# print(travel_book_urls)


# loop through all books to retrieve their details using the first function's url loop
def get_books_by_category(category_name, category_id) -> list[dict]:
    book_urls = get_books_urls_by_category(category_name, category_id)

    books = []

    for book_url in book_urls:
        book_details = get_book(book_url)
        books.append(book_details)

    return books


# Write book details to a CSV file
def write_books_to_csv(books, filename="books_by_category.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = books[0].keys() if books else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write book details
        writer.writerows(books)


book_details = get_books_by_category("travel", "2")
print(book_details)
write_books_to_csv(book_details)
