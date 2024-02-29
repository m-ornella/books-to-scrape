import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import pandas as pd

# def extract_category_infos(url) -> list[str, int]:
#     category_infos = url.split("/")[-2].split("_")
#     return category_infos


# # next page logic
# def navigate_to_next_page(soup, category_name, category_id):
#     next_button = soup.find("li", class_="next")
#     if next_button and next_button.find("a"):
#         next_page_url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/{next_button.find('a')['href']}"
#         return next_page_url
#     return None


# # get book price and category
# def get_book_price_and_category(soup):
#     books = soup.select("h3 a")

#     book_info_list = []

#     for book in books:
#         book_url = book["href"]
#         absolute_book_url = f"https://books.toscrape.com/catalogue/{book_url[9:]}"

#         page = requests.get(absolute_book_url)
#         book_soup = BeautifulSoup(page.text, "html.parser")

#         # retrieves book details using selectors
#         category = book_soup.select_one(".breadcrumb li:nth-child(3) a").text
#         price_including_tax = book_soup.select_one(
#             "table tr:nth-child(3) td"
#         ).text.replace("Â£", "")

#         book_info = {
#             "category": category,
#             "price_including_tax": price_including_tax,
#         }

#         book_info_list.append(book_info)

#     return book_info_list


# # navigate to all category urls
# def navigate_through_all_categories() -> list[dict]:
#     url = "https://books.toscrape.com/index.html"
#     page = requests.get(url)
#     soup = BeautifulSoup(page.text, "html.parser")

#     base_url = "https://books.toscrape.com/"
#     category_urls = soup.select(".nav-list li ul li a")

#     category_links = []

#     for category_url in category_urls:
#         href = base_url + category_url.get("href")
#         category_infos = extract_category_infos(href)
#         category_links.append(category_infos)

#     return category_links


# def write_category_stats_to_csv(category_stats):
#     with open(
#         "books_details_by_category.csv", mode="w", newline="", encoding="utf-8"
#     ) as csv_file:
#         fieldnames = ["Category", "Number of Books", "Average Price"]
#         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#         writer.writeheader()

#         for category, stats in category_stats.items():
#             writer.writerow(
#                 {
#                     "Category": category,
#                     "Number of Books": stats["num_books"],
#                     "Average Price": f"{stats['average_price']:.2f}",
#                 }
#             )


# def get_category_stats():
#     category_stats = {}

#     all_category_urls = navigate_through_all_categories()

#     for category_info in all_category_urls:
#         category_name, category_id = category_info
#         url = f"https://books.toscrape.com/catalogue/category/books/{category_name}_{category_id}/index.html"

#         num_books = 0
#         total_price = 0

#         while url:
#             page = requests.get(url)
#             soup = BeautifulSoup(page.text, "html.parser")

#             prices_and_categories = get_book_price_and_category(soup)

#             for price_and_category in prices_and_categories:
#                 num_books += 1
#                 total_price += float(price_and_category["price_including_tax"])

#             # check for the next page
#             url = navigate_to_next_page(soup, category_name, category_id)

#         if num_books > 0:
#             average_price = total_price / num_books
#             category_stats[category_name] = {
#                 "num_books": num_books,
#                 "average_price": average_price,
#             }

#     return category_stats


# Run the function to get category stats
# category_stats = get_category_stats()

# Print the category stats
# for category, stats in category_stats.items():
#     print(f"Category: {category}")
#     print(f"  Number of Books: {stats['num_books']}")
#     print(f"  Average Price: {stats['average_price']:.2f}")
#     print("\n")

# Run the function to write category stats to CSV
# write_category_stats_to_csv(category_stats)


# stats graphic using matplotlib
# def plot_category_stats(category_stats):
#     categories = list(category_stats.keys())
#     num_books = [stats["num_books"] for stats in category_stats.values()]

#     plt.bar(categories, num_books)
#     plt.xlabel("Category")
#     plt.ylabel("Number of Books")
#     plt.title("Number of Books in Each Category")
#     plt.xticks(rotation=45, ha="right")
#     plt.tight_layout()

#     plt.show()


# plot_category_stats(category_stats)


# circular graphic
def plot_category_stats():
    df = pd.read_csv("books_details_by_category.csv")
    top_categories = df.nlargest(20, "Number of Books")
    total_books = df["Number of Books"].sum()
    labels = [
        f"{cat} ({num} - {num/total_books*100:.1f}%)"
        for cat, num in zip(
            top_categories["Category"], top_categories["Number of Books"]
        )
    ]
    """
    # categories = list(category_stats.keys())
    num_books = [stats["Number of Books"] for stats in category_stats.values()]

    plt.pie(num_books, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Distribution of Books Across Categories")

    plt.show()
    """
    plt.figure(figsize=(10, 10))
    plt.pie(
        top_categories["Number of Books"],
        labels=labels,
        startangle=140,
        textprops={"fontsize": 6},
    )
    plt.rcParams.update({"font.size": 15})
    plt.axis("equal")
    plt.title("Top 20 Book Categories by Percentage", fontsize=10)
    plt.savefig("circle_diagram_bonus1.png")
    plt.show()


# Run the function to plot the category stats
plot_category_stats()
