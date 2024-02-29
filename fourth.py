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


# get image urls
def get_image_urls(soup):
    # Assuming the image is inside an element with class "image_container"
    image_urls = [img["src"] for img in soup.select(".image_container img[src]")]

    # Modify the URLs to remove the initial characters
    image_urls = [img[5:] for img in image_urls]

    return image_urls


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


# retrieve all image urls from all categories
def get_image_urls_from_all_categories():
    all_category_urls = navigate_through_all_categories()

    for category_info in all_category_urls:
        category_name, category_id = category_info
        url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/index.html"

        while url:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")

            # get and print image urls for the current page
            image_urls = get_image_urls(soup)
            print(f"Category: {category_name}, Page: {url}")
            for idx, img_url in enumerate(image_urls, 1):
                print(f"  Image {idx} URL: {img_url}")

            # check for the next page
            url = navigate_to_next_page(soup, category_name, category_id)


get_image_urls_from_all_categories()
