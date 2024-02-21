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
    # page_category = requests

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

    with open("book.csv", "w") as f:
        for key in book_info.keys():
            f.write("%s,%s\n" % (key, book_info[key]))

    return book_info


book_data = get_book("mesaerion-the-best-science-fiction-stories-1800-1849_983")
print(book_data)


# def get_books_by_category():
#     page = requests.get(
#         "https://books.toscrape.com/catalogue/category/books/fiction_10/index.htmll"
#     )

#     soup = BeautifulSoup(page.text, "html.parser")

#     books_by_gategory = []
#     books = soup.find_all(class_="product_pod")
#     for book in books:
#         title = soup.select_one("h1").text
#         universal_product_code = soup.select_one("table tr:first-child td").text
#         price_including_tax = soup.select_one("table tr:nth-child(3) td").text.replace(
#             "Â£", ""
#         )
#         price_excluding_tax = soup.select_one("table tr:nth-child(4) td").text.replace(
#             "Â£", ""
#         )
#         number_available = soup.select_one("table tr:nth-child(6) td").text
#         product_description = soup.select_one(".product_page > p").text
#         category = soup.select_one(".breadcrumb li:nth-child(3) a").text
#         review_rating = soup.find("p", class_="star-rating")["class"][1]
#         image_url = [img["src"] for img in soup.select(".carousel-inner img[src]")][0]
#         print(book)
#         books_by_gategory.append(
#             {
#                 "title": title,
#                 "universal_product_code": universal_product_code,
#                 "price_including_tax": price_including_tax,
#                 "price_excluding_tax": price_excluding_tax,
#                 "number_available": number_available,
#                 "product_description": product_description,
#                 "category": category,
#                 "review_rating": review_rating,
#                 "image_url": image_url,
#             }
#         )

#         return books_by_gategory


# fiction_books = get_books_by_category()
# print(fiction_books)
