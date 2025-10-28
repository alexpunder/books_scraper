from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup
from requests import RequestException, Session

from src.constants import EMPTY_DATA
from src.scraper import Scraper
from tests.conftest import TOTAL_BOOKS_PAGES, TOTAL_BOOKS_SCRAPED


class TestScraper:
    """
    Набор тестов для проверки функциональности класса Scraper.

    Тесты покрывают основные сценарии работы парсера:
    - Корректные ответы и обработка ошибок HTTP-запросов
    - Извлечение данных из HTML-страниц (название, цена, описание и т.д.)
    - Обработка граничных случаев (отсутствие данных, ошибки 404)
    - Многостраничный парсинг с пагинацией

    Attributes:
        ANY_TEST_URL: Базовый URL, используемый в тестовых запросах
    """

    ANY_TEST_URL: str = "http://books.any-test-url.com"

    def test_example_book_page_correct_response(
        self, example_book_page_correct_request
    ):
        """Тестирует корректный ответ от сервера для страницы книги.

        Проверяет, что запрос возвращает данные в ожидаемом формате.

        Args:
            example_book_page_correct_request: Фикстура с корректным HTML-ответом

        Asserts:
            - Ответ является строкой (HTML-контентом)
        """
        assert isinstance(example_book_page_correct_request, str)

    def test_example_book_page_not_found_response(
        self, scraper: Scraper, session: Session, not_found_url: str
    ):
        """Тестирует обработку HTTP-ошибки 404 (страница не найдена).

        Проверяет, что парсер корректно обрабатывает случай отсутствия страницы
        и генерирует информативное исключение.

        Args:
            scraper: Фикстура парсера
            session: Фикстура HTTP-сессии
            not_found_url: URL, возвращающий 404 ошибку

        Asserts:
            - Вызывается исключение RequestException
            - Сообщение об ошибке содержит информативный текст
            - URL присутствует в сообщении об ошибке
        """
        with pytest.raises(RequestException) as error:
            scraper._get_response_as_text(session, not_found_url)

        assert "Ошибка при попытке выполнить запрос" in str(error.value)
        assert not_found_url in str(error.value)

    def test_get_correct_book_title(
        self, scraper: Scraper, main_soup: BeautifulSoup
    ):
        """Тестирует извлечение корректного названия книги из HTML.

        Проверяет работу метода _get_title с валидными данными.

        Args:
            scraper: Фикстура парсера
            main_soup: Фикстура с корректно сформированным BeautifulSoup объектом

        Asserts:
            - Название является строкой
            - Название соответствует ожидаемому значению
        """
        title = scraper._get_title(main_soup)

        assert isinstance(title, str)
        assert title == "A Light in the Attic"

    def test_empty_book_title(
        self, scraper: Scraper, empty_title_main_soup: BeautifulSoup
    ):
        """Тестирует обработку случая отсутствия названия книги.

        Проверяет, что при невозможности извлечь название возвращается
        значение по умолчанию.

        Args:
            scraper: Фикстура парсера
            empty_title_main_soup: Фикстура с BeautifulSoup объектом без названия

        Asserts:
            - Возвращается значение EMPTY_DATA при отсутствии названия
        """
        title = scraper._get_title(empty_title_main_soup)

        assert title == EMPTY_DATA, (
            "При отсутствии названия книги, "
            f"по умолчанию должно быть значение '{EMPTY_DATA}'"
        )

    def test_get_book_data_success(
        self,
        scraper: Scraper,
        session: Session,
        example_book_full_html: str,
    ):
        """Тестирует извлечение полных данных о книге с HTML-страницы.

        Проверяет корректность работы метода _get_book_data при парсинге
        полноценной HTML-страницы книги. Тест использует мок для подмены
        HTTP-запроса и проверяет что все компоненты данных извлекаются правильно.

        Проверяемые данные:
        - Основная информация: название, цена, доступность, рейтинг, описание
        - Таблица характеристик: UPC, тип продукта, цены с налогом и без, налог, отзывы

        Ожидаемые значения соответствуют данным в фикстуре example_book_full_html.
        """
        with patch.object(
            scraper,
            "_get_response_as_text",
            return_value=example_book_full_html,
        ):
            result = scraper._get_book_data(session, self.ANY_TEST_URL)

            assert isinstance(result, dict)

            assert result["Title"] == "A Light in the Attic"
            assert result["Price"] == "£51.77"
            assert result["Available"] == "22"
            assert result["Rating"] == "3"
            assert (
                result["Description"]
                == "It's hard to imagine a world without A Light in the Attic."
            )

            assert isinstance(result["Info_table"], dict)

            assert result["Info_table"]["UPC"] == "a897fe39b1053632"
            assert result["Info_table"]["Product Type"] == "Books"
            assert result["Info_table"]["Price (excl. tax)"] == "£51.77"
            assert result["Info_table"]["Price (incl. tax)"] == "£51.77"
            assert result["Info_table"]["Tax"] == "£0.00"
            assert result["Info_table"]["Number of reviews"] == "0"

    def test_get_all_books_data_success(
        self,
        scraper: Scraper,
        page1_html_with_next2: str,
        page2_html_with_next3: str,
        page3_html_without_next: str,
        books_titles: list[dict[str, str]],
    ):
        """Тестирует полный цикл парсинга с многостраничным каталогом.

        Проверяет:
        - Корректность обхода страниц пагинации
        - Обработку всех книг со всех страниц
        - Формирование итогового списка данных
        """
        with (
            patch.object(scraper, "_get_response_as_text") as mock_get_text,
            patch.object(scraper, "_get_book_data") as mock_get_book_data,
        ):
            mock_get_text.side_effect = [
                page1_html_with_next2,
                page2_html_with_next3,
                page3_html_without_next,
            ]

            mock_get_book_data.side_effect = books_titles

            books = scraper.scrape_books()

            assert isinstance(books, list)
            assert all(isinstance(book, dict) for book in books)

            assert len(books) == TOTAL_BOOKS_SCRAPED

            assert books[0]["Title"] == "Book 1"
            assert books[4]["Title"] == "Book 5"

            assert mock_get_text.call_count == TOTAL_BOOKS_PAGES
            assert mock_get_book_data.call_count == TOTAL_BOOKS_SCRAPED
