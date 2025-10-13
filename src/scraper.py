import json
import time
import schedule

from typing import Any

from bs4 import BeautifulSoup, Tag
from requests import Session, Response
from requests.exceptions import RequestException

from constants import (
    BASE_URL,
    FILE_PATH,
    RATING_MAP,
    RESPONSE_TIMEOUT,
    SAVE_DIR_PATH,
    START_CATALOGUE_PAGE_URL,
    LINK_NOT_FOUND,
    EMPTY_DATA,
    CLEAN_CURRENCY,
    TASK_START_TIME,
    UNKNOWN_RATING,
    UNKNOWN_RATING_VALUE,
    WAITING_TIME,
)


class Parcer:
    # TODO: написать docstring

    def __init__(self):
        self.start_page = START_CATALOGUE_PAGE_URL

    def _get_session(self, *args, **kwargs) -> Session:
        return Session(*args, **kwargs)

    def _get_response_as_text(self, session: Session, url: str) -> Response:
        try:
            response = session.get(url, timeout=RESPONSE_TIMEOUT)
            response.raise_for_status()
            return response.text
        except RequestException as error:
            raise RequestException(f"Ошибка при попытке выполнить запрос к {url}: {error}")

    def _get_soup(self, text: str, pars_lib: str = "html.parser") -> BeautifulSoup:
        return BeautifulSoup(text, pars_lib)

    def _get_next_page(self, soup: BeautifulSoup) -> str | None:
        next = soup.select_one("li.next a")
        return next.get("href", LINK_NOT_FOUND) if next else None

    def _get_books_redirections(self, soup: BeautifulSoup) -> list[str]:
        return [
            a.get("href", LINK_NOT_FOUND)
            for a in soup.select("section ol.row div.image_container a")
        ]

    def _get_title(self, main_data: Tag) -> str:
        title = main_data.find("h1")
        return title.get_text(strip=True) if title else EMPTY_DATA

    def _get_price(self, main_data: Tag) -> str:
        price = main_data.find(class_="price_color")
        return price.text.replace(CLEAN_CURRENCY, "") if price else EMPTY_DATA

    def _formatter_avialable(self, available_data: str):
        return "".join(i for i in available_data if i.isdigit())

    def _get_available(self, main_data: Tag) -> str | None:
        available = main_data.find(class_="instock availability")

        if available:
            return self._formatter_avialable(available.get_text(strip=True))

        return EMPTY_DATA

    def _get_rating(self, main_data: Tag) -> str:
        rating_class = main_data.find(class_="star-rating")
                
        if not rating_class:
            return EMPTY_DATA
        
        _, rating = rating_class.get("class", UNKNOWN_RATING)
        return RATING_MAP.get(rating, UNKNOWN_RATING_VALUE)

    def _get_description(self, soup: Tag) -> str:
        sub_header = soup.find(id="product_description")

        if not sub_header:
            return EMPTY_DATA

        description = sub_header.find_next("p")
        return description.get_text(strip=True) if description else EMPTY_DATA

    def _get_info_table(self, soup: Tag) -> dict[str, Any]:
        product_table = soup.find(class_="table table-striped")

        if not product_table:
            return {}

        rows = product_table.select("tr")
        info_table = {}
        for row in rows:
            key = row.select_one("th").get_text(strip=True)
            value = row.select_one("td").get_text(strip=True)

            if "Price" in key or "Tax" in key:
                value = value.replace(CLEAN_CURRENCY, "")

            if "Availability" in key:
                continue

            info_table[key] = value

        return info_table

    @staticmethod
    def _save_books_data_as_file(result_data: list[dict[str, Any]]):
        SAVE_DIR_PATH.mkdir(parents=True, exist_ok=True)
        with open(FILE_PATH, mode="w", encoding="utf-8") as write:
            json.dump(result_data, write, ensure_ascii=False, indent=2)

    def _get_book_data(self, session: Session, book_url: str) -> dict[str, Any]:
        text = self._get_response_as_text(session, book_url)
        soup = self._get_soup(text)

        main_data = soup.find(class_="col-sm-6 product_main")

        if not main_data:
            raise ValueError("Не найдена основная информация о книге")

        info_table = self._get_info_table(soup)

        return {
            "Title": self._get_title(main_data),
            "Price": self._get_price(main_data),
            "Available": self._get_available(main_data),
            "Rating": self._get_rating(main_data),
            "Description": self._get_description(soup),
            **info_table,
        }

    def scrape_books(self, is_save: bool = False) -> list[dict[str, Any]]:
        with self._get_session() as session:
            text = self._get_response_as_text(session, self.start_page)
            soup = self._get_soup(text)

            scraped_books = []
            while True:
                books_redirections = self._get_books_redirections(soup)
                for book_redirect in books_redirections:
                    book_url = BASE_URL + book_redirect
                    scraped_book = self._get_book_data(session, book_url)
                    scraped_books.append(scraped_book)

                next_page = self._get_next_page(soup)
                if not next_page:
                    break

                next_page_url = BASE_URL + next_page
                text = self._get_response_as_text(session, next_page_url)
                soup = self._get_soup(text)

        if is_save:
            self._save_books_data_as_file(scraped_books)

        return scraped_books

    def create_dayly_task(self, start_time: str = TASK_START_TIME) -> schedule.Job:
        schedule.every().day.at(start_time).do(self.scrape_books, is_save=True)


if __name__ == "__main__":
    book_parcer = Parcer()
    book_parcer.create_dayly_task()

    try:
        while True:
            schedule.run_pending()
            next_run = schedule.idle_seconds()
            time.sleep(min(next_run, WAITING_TIME))
    except Exception as error:
        print(f"Возникла ошибка при парсинге данных: {error}")
    except KeyboardInterrupt:
        print("Ручной выход из программы")
 

# def get_book_data(book_url: str) -> dict:
#     """
#     МЕСТО ДЛЯ ДОКУМЕНТАЦИИ
#     """
#     # НАЧАЛО ВАШЕГО РЕШЕНИЯ
#     book_data = {}
#     response = Session().get(book_url)
#     response.raise_for_status()
#     soup = BeautifulSoup(response.text, "html.parser")

#     # основная информация
#     main_data = soup.find(class_="col-sm-6 product_main")

#     if not main_data:
#         raise ValueError("Не найдена основная информация о книге")

#     title = main_data.find("h1")
#     book_data["title"] = title.get_text(strip=True) if title else const.EMPTY_DATA

#     price = main_data.find(class_="price_color")
#     if price:
#         price = price.text.replace("Â", "")
#         book_data["price"] = price
#     else:
#         book_data["price"] = const.EMPTY_DATA

#     available = main_data.find(class_="instock availability")
#     if available:
#         available_data = available.get_text(strip=True)
#         available = int("".join(i for i in available_data if i.isdigit()))
#         book_data["available"] = available
#     else:
#         book_data["available"] = const.EMPTY_DATA

#     rating_class = main_data.find(class_="star-rating")
#     _, rating = rating_class["class"]
#     book_data["rating"] = const.RATING_MAP.get(rating, const.UNKNOWN_RATING) if rating else const.EMPTY_DATA

#     # описание
#     sub_header = soup.find(id="product_description")
#     description = sub_header.find_next("p")
#     book_data["description"] = description.get_text(strip=True) if description else const.EMPTY_DATA

#     # таблица
#     product_table = soup.find(class_="table table-striped")
#     rows = product_table.select("tr")
#     book_table_info = {}
#     for row in rows:
#         key = row.select_one("th").get_text(strip=True)
#         value = row.select_one("td").get_text(strip=True)

#         if "Price" in key or "Tax" in key:
#           value = value.replace("Â", "")

#         book_table_info[key] = value

#     book_data["product_info"] = book_table_info
