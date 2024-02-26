import requests
from bs4 import BeautifulSoup
import csv

# from second import (
#     # navigate_to_next_page,
#     # get_books_urls_by_category,
#     # get_books_by_category,
# )


# retrieving details from all books


# navigate to all category urls
def navigate_through_all_categories(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    base_url = "https://books.toscrape.com/"

    category_urls = soup.select(".nav-list li ul li a")

    category_links = []

    for category_url in category_urls:
        href = base_url + category_url.get("href")

        category_links.append(href)

    return category_links


urls = navigate_through_all_categories("https://books.toscrape.com/index.html")
print(urls)
