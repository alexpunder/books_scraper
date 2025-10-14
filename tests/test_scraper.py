from unittest.mock import patch
from bs4 import BeautifulSoup
import pytest

from requests import RequestException, Session

from src.constants import EMPTY_DATA
from src.scraper import Scraper
from tests.conftest import TOTAL_BOOKS_PAGES, TOTAL_BOOKS_SCRAPED


class TestScraper:
    ANY_TEST_URL: str = "http://books.any-test-url.com"

    def test_example_book_page_correct_response(
        self, example_book_page_correct_request
    ):
        assert isinstance(example_book_page_correct_request, str)

    def test_example_book_page_not_found_response(
        self, scraper: Scraper, session: Session, not_found_url: str
    ):
        with pytest.raises(RequestException) as error:
            scraper._get_response_as_text(session, not_found_url)

        assert "Ошибка при попытке выполнить запрос" in str(error.value)
        assert not_found_url in str(error.value)

    def test_get_correct_book_title(
        self, scraper: Scraper, main_soup: BeautifulSoup
    ):
        title = scraper._get_title(main_soup)

        assert isinstance(title, str)
        assert title == "A Light in the Attic"

    def test_empty_book_title(
        self, scraper: Scraper, empty_title_main_soup: BeautifulSoup
    ):
        title = scraper._get_title(empty_title_main_soup)

        assert title == EMPTY_DATA, (
            f"При отсутствии названия книги, по умолчанию должно быть значение '{EMPTY_DATA}'"
        )

    def test_get_book_data_success(
        self,
        scraper: Scraper,
        session: Session,
        example_book_full_html: str,
    ):
        with patch.object(
            scraper,
            "_get_response_as_text",
            return_value=example_book_full_html,
        ):
            result = scraper._get_book_data(session, self.ANY_TEST_URL)

            assert result["Title"] == "A Light in the Attic"
            assert result["Price"] == "£51.77"
            assert result["Available"] == "22"
            assert result["Rating"] == "3"
            assert (
                result["Description"]
                == "It's hard to imagine a world without A Light in the Attic."
            )

            assert result["UPC"] == "a897fe39b1053632"
            assert result["Product Type"] == "Books"
            assert result["Price (excl. tax)"] == "£51.77"
            assert result["Price (incl. tax)"] == "£51.77"
            assert result["Tax"] == "£0.00"
            assert result["Number of reviews"] == "0"

    def test_get_all_books_data_success(
        self,
        scraper: Scraper,
        page1_html_with_next2: str,
        page2_html_with_next3: str,
        page3_html_without_next: str,
        books_titles: list[dict[str, str]],
    ):
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
