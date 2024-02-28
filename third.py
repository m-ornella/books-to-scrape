import requests
from bs4 import BeautifulSoup
import csv

from first import get_book


# retrieving details from all books


def navigate_to_next_page(soup, category_name, category_id):
    next_button = soup.find("li", class_="next")
    if next_button and next_button.find("a"):
        next_page_url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/{next_button.find('a')['href']}"
        return next_page_url
    return None


# navigate to all category urls
def navigate_through_all_categories() -> list[str]:

    url = "https://books.toscrape.com/index.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    base_url = "https://books.toscrape.com/"

    category_urls = soup.select(".nav-list li ul li a")

    category_links = []

    for category_url in category_urls:
        href = base_url + category_url.get("href")
        category_infos = extract_category_infos(href)
        category_links.append(category_infos)

    return category_links


# loop through all book urls in travel category
def get_books_urls_by_category(category_name, category_id) -> list[str]:
    base_url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/index.html"
    current_page_url = base_url

    book_urls = []

    while current_page_url:
        page = requests.get(current_page_url)
        soup = BeautifulSoup(page.text, "html.parser")

        for book in soup.find_all("article", class_="product_pod"):
            link = book.find("a")
            book_url = link.get("href")
            absolute_book_url = f"https://books.toscrape.com/catalogue/{book_url[9:]}"
            book_urls.append(absolute_book_url)

        # Navigate to the next page if available
        current_page_url = navigate_to_next_page(soup, category_name, category_id)

    return book_urls


# loop through all books to retrieve their details using the first function's url loop
def get_books_by_category(category_name, category_id) -> list[dict]:
    book_urls = get_books_urls_by_category(category_name, category_id)

    books = []

    for book_url in book_urls:
        book_details = get_book(book_url)
        books.append(book_details)

    return books


def extract_category_infos(url) -> list[str, int]:
    category_infos = url.split("/")[-2].split("_")

    return category_infos


# get all books infos from all categories
def get_all_books_from_all_categories() -> list[dict]:
    categories_infos_list = navigate_through_all_categories()
    all_books = []

    for category_infos in categories_infos_list:
        category_name = category_infos[0]
        category_id = category_infos[1]
        all_books_details = get_books_by_category(category_name, category_id)
        # print(category_infos)
        all_books.append(all_books_details)
        print(all_books_details)

    return all_books


# Write book details to a CSV file
def write_all_books_to_csv(all_books_details, filename="all_books.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = all_books_details[0].keys() if all_books_details else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write book details
        writer.writerows(all_books_details)


# testing navigate_through_all_categories()
# urls = navigate_through_all_categories()
# print(urls)

all_books = get_all_books_from_all_categories()
print(all_books)
