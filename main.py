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


def get_book(sub_url):

    base_url = "https://books.toscrape.com/catalogue/"
    category_slug = "/category"
    page = requests.get(base_url + sub_url + "/index.html")

    soup = BeautifulSoup(page.text, "html.parser")

    title = soup.select_one("h1").text
    universal_product_code = soup.select_one("table tr:first-child td").text
    price_including_tax = soup.select_one("table tr:nth-child(3) td").text.replace(
        "Â£", ""
    )
    price_excluding_tax = soup.select_one("table tr:nth-child(4) td").text.replace(
        "Â£", ""
    )
    number_available = soup.select_one("table tr:nth-child(6) td").text
    product_description = soup.select_one(".product_page > p").text
    category = soup.select_one(".breadcrumb li:nth-child(3) a").text
    review_rating = soup.find("p", class_="star-rating")["class"][1]
    image_url = [img["src"] for img in soup.select(".carousel-inner img[src]")][0]

    book_info = {
        "title": title,
        "universal_product_code": universal_product_code,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url,
    }

    return book_info


def write_book_info_to_csv(book_info, filename="book.csv"):
    with open(filename, "w") as f:
        for key, value in book_info.items():
            f.write(f"{key},{value}\n")


book_data = get_book("mesaerion-the-best-science-fiction-stories-1800-1849_983")
print(book_data)


def get_books_by_category():
    get_book(sub_url="/category/books/fiction_10")
