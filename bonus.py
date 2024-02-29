import requests
from bs4 import BeautifulSoup


def extract_category_infos(url) -> list[str, int]:
    category_infos = url.split("/")[-2].split("_")
    return category_infos


# next page logic
def navigate_to_next_page(soup, category_name, category_id):
    next_button = soup.find("li", class_="next")
    if next_button and next_button.find("a"):
        next_page_url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/{next_button.find('a')['href']}"
        return next_page_url
    return None


# get book price and category
def get_book_price_and_category(soup):
    books = soup.select("h3 a")

    book_info_list = []

    for book in books:
        book_url = book["href"]
        absolute_book_url = f"https://books.toscrape.com/catalogue/{book_url[9:]}"

        page = requests.get(absolute_book_url)
        book_soup = BeautifulSoup(page.text, "html.parser")

        # retrieves book details using selectors
        category = book_soup.select_one(".breadcrumb li:nth-child(3) a").text
        price_including_tax = book_soup.select_one(
            "table tr:nth-child(3) td"
        ).text.replace("Â£", "")

        book_info = {
            "price_including_tax": price_including_tax,
            "category": category,
        }

        book_info_list.append(book_info)

    return book_info_list


# navigate to all category urls
def navigate_through_all_categories() -> list[dict]:
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


def get_book_price_and_category_from_all_pages():
    all_category_urls = navigate_through_all_categories()

    for category_info in all_category_urls:
        category_name, category_id = category_info
        url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/index.html"

        while url:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")

            prices_and_categories = get_book_price_and_category(soup)

            for price_and_category in prices_and_categories:
                print(price_and_category)

            # check for the next page
            url = navigate_to_next_page(soup, category_name, category_id)


def get_book_stats_by_category():
    category_stats = {}

    all_category_urls = navigate_through_all_categories()

    for category_info in all_category_urls:
        category_name, category_id = category_info
        url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/index.html"

        num_books = 0
        total_price = 0

        while url:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")

            prices_and_categories = get_book_price_and_category(soup)

            for price_and_category in prices_and_categories:
                num_books += 1
                total_price += float(price_and_category["price_including_tax"])

            # check for the next page
            url = navigate_to_next_page(soup, category_name, category_id)

        if num_books > 0:
            average_price = total_price / num_books
            category_stats[category_name] = {
                "num_books": num_books,
                "average_price": average_price,
            }

    return category_stats


category_stats = get_book_stats_by_category()
for category, stats in category_stats.items():
    print(f"Category: {category}")
    print(f"  Number of Books: {stats['num_books']}")
    print(f"  Average Price: {stats['average_price']:.2f}")
    print("\n")
