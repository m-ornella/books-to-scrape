import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os


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
    image_urls = [img["src"] for img in soup.select(".image_container img[src]")]
    image_urls = [img[11:] for img in image_urls]

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


# download images into '/images' folder
def download_image(url, folder_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Extract the filename from the URL
        filename = url.split("/")[-1]

        # Save the image to the specified folder
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


# loop through all categories and download images
def get_image_urls_from_all_categories():
    all_category_urls = navigate_through_all_categories()

    for category_info in all_category_urls:
        category_name, category_id = category_info
        url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/index.html"

        while url:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")

            image_urls = get_image_urls(soup)

            for img_url in image_urls:
                # download each image into '/images' folder
                download_image(urljoin(url, img_url), "images")

            # check for the next page
            url = navigate_to_next_page(soup, category_name, category_id)


get_image_urls_from_all_categories()
