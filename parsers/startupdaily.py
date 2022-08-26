import requests
from bs4 import BeautifulSoup
import csv
import os.path
from dataclasses import dataclass


class UserAgent:
    # Their server gives 403 error for users without user-agent
    def __init__(self, agent_value: str = "Python3"):
        self.user_agent = agent_value

    def as_json(self):
        return {"User-Agent": self.user_agent}


# bad: global variable
transport_words = open("parsers/transport_words.txt").read().split("\n")


def is_transport_article(text):
    for word in text:
        if word.lower() in transport_words:
            return True
    return False


def prepare_file(path: str):

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="|")
        header_table = (
            "url",
            "title",
            "date",
            "author",
            "tags",
            "text",
            "transport",
            "transport_processing",
        )
        writer.writerow(header_table)


def get_max_page_number(headers) -> int:
    """Gets the quantity of pages with content

    Returns
    -------
    int
        the number of pages.
    """
    req = requests.get(
        "https://www.startupdaily.net/news/page/0/",
        headers=headers,
    )
    soup = BeautifulSoup(req.text, "html.parser")
    pages_count_links = soup.find(class_="pagination").find_all("a")
    if len(pages_count_links) >= 2:
        # well, the last page must be the last number
        return int(pages_count_links[-1].text)


def get_correct_date(date: str):
    date_mapping = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "november": 10,
        "december": 11,
    }
    date = date.replace(",", "")
    date = date.split()
    month = date_mapping[date[0].lower()]
    year = date[-1]
    day = date[1]
    return day + "/" + str(month) + "/" + year


# shared data could be a class, again
def parse_startup_page(url: str, headers, path_to_csv: str) -> str:
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    title = soup.find(class_="entry-title single-title").get_text()
    author = soup.find(rel="author").get_text()
    date = (
        soup.find(class_="post-top-meta")
        .find_all(text=True, recursive=False)[1]
        .replace("-", " ")
        .strip()
        .lower()
    )

    formatted_date = get_correct_date(date)

    article_text = soup.find(class_="entry-content").get_text()
    tag_objects = soup.find_all(class_="tag-link")
    tag_list = [object.get_text() for object in tag_objects]

    # ez to get the dictionary as the page_data parameter, aka remove page_data...
    header_table = (
        url,
        title,
        formatted_date,
        author,
        ", ".join(tag_list),
        article_text.strip().replace("\n", " ").replace("|", ""),
        "yes" if is_transport_article(article_text) else "no",
        "",
    )
    with open(path_to_csv, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow(header_table)


def parse_block_page(url, headers, path_to_csv: str):

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    links = soup.find_all(rel="bookmark")
    for link in links:
        parse_startup_page(link["href"], headers, path_to_csv)


def start_collecting(headers, path_to_csv: str):
    page_num = 0
    pages_url = "https://www.startupdaily.net/news/page/{0}/"
    max_page_num = get_max_page_number(headers)
    while page_num <= max_page_num:
        parse_block_page(pages_url.format(page_num), headers, path_to_csv)
        page_num += 1


def main():
    prepare_file("parsers/out.csv")
    user_agent = UserAgent().as_json()
    start_collecting(user_agent, "parsers/out.csv")


if __name__ == "__main__":
    main()
