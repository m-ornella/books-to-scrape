import requests
from bs4 import BeautifulSoup
import csv

# product_page_url
# universal_product_code [upc]
# title
# price_including_tax
# price_excluding_tax
# number_available
# product_description
# category
# review_rating
# image_url


def write_book_info_to_csv(book_info, filename="book.csv"):
    with open(filename, "w") as f:
        for key, value in book_info.items():
            f.write(f"{key},{value}\n")


# book_data = get_book("mesaerion-the-best-science-fiction-stories-1800-1849_983")
# print(book_data)


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

    return book_urls


travel_book_urls = get_books_urls_by_category("travel", "2")
print(travel_book_urls)


# def get_books_by_category():
#    get_book


#     return fiction_books


# fiction_books = get_books_by_category()
# print(fiction_books)
