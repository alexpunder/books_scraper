import json
import time
import schedule

from typing import Any

from bs4 import BeautifulSoup, Tag
from requests import Session
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
    DELAY,
)


class Scraper:
    """Парсер для сбора данных о книгах с сайта books.toscrape.com.

    Класс предоставляет функциональность для обхода каталога книг,
    извлечения детальной информации о каждой книге и сохранения результатов.
    """

    def _get_session(self, *args, **kwargs) -> Session:
        """Создает и возвращает новую сессию для HTTP-запросов.

        Returns:
            Session: Объект сессии для выполнения HTTP-запросов.
        """
        return Session(*args, **kwargs)

    def _get_response_as_text(self, session: Session, url: str) -> str:
        """Выполняет HTTP-запрос и возвращает текст ответа.

        Args:
            session (Session): Сессия для выполнения запроса.
            url (str): URL для запроса.

        Raises:
            RequestException: Если произошла ошибка при выполнении запроса
                или получен статус код ошибки.

        Returns:
            str: Текст HTML-страницы.
        """
        try:
            response = session.get(url, timeout=RESPONSE_TIMEOUT)
            response.raise_for_status()
            return response.text
        except RequestException as error:
            raise RequestException(
                f"Ошибка при попытке выполнить запрос к {url}: {error}"
            )

    def _get_soup(
        self, text: str, pars_lib: str = "html.parser"
    ) -> BeautifulSoup:
        """Создает объект BeautifulSoup из HTML-текста.

        Args:
            text (str): HTML-текст для парсинга.
            pars_lib (str, optional): Парсер для BeautifulSoup.
                Defaults to "html.parser".

        Returns:
            BeautifulSoup: Объект для парсинга HTML.
        """
        return BeautifulSoup(text, pars_lib)

    def _get_next_page(self, soup: BeautifulSoup) -> str | None:
        """Извлекает URL следующей страницы каталога.

        Args:
            soup (BeautifulSoup): Объект BeautifulSoup текущей страницы.

        Returns:
            str | None: URL следующей страницы или None, если это последняя страница.
        """
        next = soup.select_one("li.next a")
        return next.get("href", LINK_NOT_FOUND) if next else None

    def _get_books_redirections(self, soup: BeautifulSoup) -> list[str]:
        """Извлекает список URL книг со страницы каталога.

        Args:
            soup (BeautifulSoup): Объект BeautifulSoup страницы каталога.

        Returns:
            list[str]: Список относительных URL страниц книг.
        """
        return [
            a.get("href", LINK_NOT_FOUND)
            for a in soup.select("section ol.row div.image_container a")
        ]

    def _get_title(self, main_data: Tag) -> str:
        """Извлекает название книги из основного блока информации.

        Args:
            main_data (Tag): HTML-элемент с основной информацией о книге.

        Returns:
            str: Название книги или EMPTY_DATA, если не найдено.
        """
        title = main_data.find("h1")
        return title.get_text(strip=True) if title else EMPTY_DATA

    def _get_price(self, main_data: Tag) -> str:
        """Извлекает цену книги из основного блока информации.

        Args:
            main_data (Tag): HTML-элемент с основной информацией о книге.

        Returns:
            str: Цена книги без символа валюты или EMPTY_DATA, если не найдено.
        """
        price = main_data.find(class_="price_color")
        return price.text.replace(CLEAN_CURRENCY, "") if price else EMPTY_DATA

    def _formatter_avialable(self, available_data: str):
        """Извлекает числовое значение доступности из строки.

        Args:
            available_data (str): Строка с информацией о доступности.

        Returns:
            str: Число доступных копий в виде строки.
        """
        return "".join(i for i in available_data if i.isdigit())

    def _get_available(self, main_data: Tag) -> str | None:
        """Извлекает количество доступных копий книги.

        Args:
            main_data (Tag): HTML-элемент с основной информацией о книге.

        Returns:
            str | None: Количество доступных копий или EMPTY_DATA, если не найдено.
        """
        available = main_data.find(class_="instock availability")

        if available:
            return self._formatter_avialable(available.get_text(strip=True))

        return EMPTY_DATA

    def _get_rating(self, main_data: Tag) -> str:
        """Извлекает рейтинг книги из CSS-классов.

        Args:
            main_data (Tag): HTML-элемент с основной информацией о книге.

        Returns:
            str: Числовой рейтинг от 1 до 5 или UNKNOWN_RATING_VALUE, если не найден.
        """
        rating_class = main_data.find(class_="star-rating")

        if not rating_class:
            return EMPTY_DATA

        _, rating = rating_class.get("class", UNKNOWN_RATING)
        return RATING_MAP.get(rating, UNKNOWN_RATING_VALUE)

    def _get_description(self, soup: Tag) -> str:
        """Извлекает описание книги.

        Args:
            soup (Tag): Объект BeautifulSoup страницы книги.

        Returns:
            str: Описание книги или EMPTY_DATA, если не найдено.
        """
        sub_header = soup.find(id="product_description")

        if not sub_header:
            return EMPTY_DATA

        description = sub_header.find_next("p")
        return description.get_text(strip=True) if description else EMPTY_DATA

    def _get_info_table(self, soup: Tag) -> dict[str, Any]:
        """Извлекает дополнительную информацию из таблицы характеристик.

        Args:
            soup (Tag): Объект BeautifulSoup страницы книги.

        Returns:
            dict[str, Any]: Словарь с характеристиками книги.
        """
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
        """Сохраняет данные о книгах в JSON-файл.

        Args:
            result_data (list[dict[str, Any]]): Список словарей с данными о книгах.
        """
        SAVE_DIR_PATH.mkdir(parents=True, exist_ok=True)
        with open(FILE_PATH, mode="w", encoding="utf-8") as write:
            json.dump(result_data, write, ensure_ascii=False, indent=2)

    def _get_book_data(
        self, session: Session, book_url: str
    ) -> dict[str, Any]:
        """Извлекает полную информацию о книге с её страницы.

        Args:
            session (Session): Сессия для HTTP-запросов.
            book_url (str): URL страницы книги.

        Raises:
            ValueError: Если не найдена основная информация о книге.

        Returns:
            dict[str, Any]: Словарь с полной информацией о книге.
        """
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
        """Парсит данные о всех книгах из каталога.

        Обходит все страницы каталога, извлекает информацию о каждой книге
        и возвращает список с данными. Может сохранять результаты в файл.

        Args:
            is_save (bool, optional): Сохранять ли данные в файл. Defaults to False.

        Returns:
            list[dict[str, Any]]: Список словарей с данными о книгах.
        """
        with self._get_session() as session:
            text = self._get_response_as_text(
                session, START_CATALOGUE_PAGE_URL
            )
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

    def create_dayly_task(
        self, start_time: str = TASK_START_TIME
    ) -> schedule.Job:
        """Создает ежедневную задачу для автоматического парсинга.

        Args:
            start_time (str, optional): Время запуска в формате HH:MM.
                Defaults to TASK_START_TIME.

        Returns:
            schedule.Job: Объект запланированной задачи.
        """
        schedule.every().day.at(start_time).do(self.scrape_books, is_save=True)


if __name__ == "__main__":
    book_scraper = Scraper()
    book_scraper.create_dayly_task()

    try:
        while True:
            schedule.run_pending()
            next_run = schedule.idle_seconds()
            time.sleep(min(next_run, DELAY))
    except Exception as error:
        print(f"Возникла ошибка при парсинге данных: {error}")
    except KeyboardInterrupt:
        print("Ручной выход из программы")
