import requests
from bs4 import BeautifulSoup


# get book price and category
def get_book_price_and_category(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    # retrieves book details using selectors
    category = soup.select_one(".breadcrumb li:nth-child(3) a").text
    price_including_tax = soup.select_one("table tr:nth-child(3) td").text.replace(
        "Â£", ""
    )

    book_info = {
        "price_including_tax": price_including_tax,
        "category": category,
    }

    return book_info


book_details = get_book_price_and_category(
    "https://books.toscrape.com/catalogue/amid-the-chaos_788/index.html"
)

print(book_details)
