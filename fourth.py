import requests
from bs4 import BeautifulSoup


# from third import extract_category_infos
def extract_category_infos(url) -> list[str, int]:
    category_infos = url.split("/")[-2].split("_")

    return category_infos


# get image urls
def get_image_url():
    page = requests.get("https://books.toscrape.com/index.html")
    soup = BeautifulSoup(page.text, "html.parser")

    # Assuming the image is inside an element with class "image_container"
    image_urls = [img["src"] for img in soup.select(".image_container img[src]")]

    for image_url in image_urls:
        image_split_links = image_url
        print(image_split_links)

    return image_split_links


# url = get_image_url()
# print(url)


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


# all_category_urls = navigate_through_all_categories()
# print(all_category_urls)


def get_image_urls_from_all_categories(category_name, category_id):
    url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/index.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    category_urls_infos = navigate_through_all_categories()

    for category_urls_info in category_urls_infos:
        print(category_urls_info)
        image_urls = get_image_url()
        print(image_urls)

    return category_urls_info


categery_info = get_image_urls_from_all_categories("travel", "2")
