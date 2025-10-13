import time
import requests
import schedule
from bs4 import BeautifulSoup


BASE_URL: str = "https://books.toscrape.com/catalogue/"
START_CATALOGUE_PAGE_URL: str = BASE_URL + "page-1.html"
EXAMPLE_BOOK_PAGE_URL: str = BASE_URL + "a-light-in-the-attic_1000/index.html"
N_PAGES: int = 50


def get_book_data(self, book_url: str) -> dict:
    pass


if __name__ == "__main__":
    pass
