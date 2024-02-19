import requests
from bs4 import BeautifulSoup


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

page = requests.get(
    "https://books.toscrape.com/catalogue/mesaerion-the-best-science-fiction-stories-1800-1849_983/index.html"
)


soup = BeautifulSoup(page.text, "html.parser")

price = soup.css.select(".product_main .price_color")

print(price)
