from bs4 import BeautifulSoup
import pytest
from requests import Session

from src.scraper import Scraper


EXAMPLE_BOOK_PAGE: str = (
    "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
)
BAD_URL_MIXIN: str = "/something-bad"
TOTAL_BOOKS_SCRAPED: int = 9
TOTAL_BOOKS_PAGES: int = 3


@pytest.fixture
def scraper() -> Scraper:
    return Scraper()


@pytest.fixture
def session(scraper: Scraper) -> Session:
    return scraper.session


@pytest.fixture
def example_book_page_correct_request(
    scraper: Scraper, session: Session
) -> str:
    return scraper._get_response_as_text(session, EXAMPLE_BOOK_PAGE)


@pytest.fixture
def not_found_url() -> str:
    return EXAMPLE_BOOK_PAGE + BAD_URL_MIXIN


@pytest.fixture
def book_main_data_html() -> str:
    return """
    <div class="col-sm-6 product_main">
      <h1>A Light in the Attic</h1>
      <p class="price_color">£51.77</p>
      <p class="instock availability">
        <i class="icon-ok"></i>
          In stock (22 available)
      </p>
      <p class="star-rating Three"></p>
    """


@pytest.fixture
def empty_title_book_main_data_html() -> str:
    return """
    <div class="col-sm-6 product_main">
      <p class="price_color">£51.77</p>
      <p class="instock availability">
        <i class="icon-ok"></i>
          In stock (22 available)
      </p>
      <p class="star-rating Three"></p>
    """


@pytest.fixture
def book_description_html() -> str:
    return """
    <div id="product_description" class="sub-header">
      <h2>Product Description</h2>
    </div>
    <p>It's hard to imagine a world without A Light in the Attic.</p>
    """


@pytest.fixture
def info_table_html() -> str:
    return """
    <table class="table table-striped">
    <tbody>
        <tr>
        <th>UPC</th><td>a897fe39b1053632</td>
        </tr>
        <tr>
        <th>Product Type</th><td>Books</td>
        </tr>
        <tr>
        <th>Price (excl. tax)</th><td>£51.77</td>
        </tr>
        <tr>
        <th>Price (incl. tax)</th><td>£51.77</td>
        </tr>
        <tr>
        <th>Tax</th><td>£0.00</td>
        </tr>
        <tr>
        <th>Availability</th>
        <td>In stock (22 available)</td>
        </tr>
        <tr>
        <th>Number of reviews</th>
        <td>0</td>
        </tr>
    </tbody>
    </table>
    """


@pytest.fixture
def page1_html_with_next2():
    return """
    <html>
      <section>
        <ol class="row">
          <li><div class="image_container"><a href="/book1.html"></a></div></li>
          <li><div class="image_container"><a href="/book2.html"></a></div></li>
          <li><div class="image_container"><a href="/book3.html"></a></div></li>
        </ol>
      </section>
      <li class="next"><a href="/page2.html">next</a></li>
    </html>
    """


@pytest.fixture
def page2_html_with_next3():
    return """
    <html>
      <section>
        <ol class="row">
          <li><div class="image_container"><a href="/book4.html"></a></div></li>
          <li><div class="image_container"><a href="/book5.html"></a></div></li>
          <li><div class="image_container"><a href="/book6.html"></a></div></li>
        </ol>
      </section>
      <li class="next"><a href="/page3.html">next</a></li>
    </html>
    """


@pytest.fixture
def page3_html_without_next():
    return """
    <html>
      <section>
        <ol class="row">
          <li><div class="image_container"><a href="/book7.html"></a></div></li>
          <li><div class="image_container"><a href="/book8.html"></a></div></li>
          <li><div class="image_container"><a href="/book9.html"></a></div></li>
        </ol>
      </section>
    </html>
    """


@pytest.fixture
def books_titles() -> list[dict[str, str]]:
    return [{"Title": f"Book {i}"} for i in range(1, TOTAL_BOOKS_SCRAPED + 1)]


@pytest.fixture
def main_soup(scraper: Scraper, book_main_data_html: str) -> BeautifulSoup:
    return scraper._get_soup(book_main_data_html)


@pytest.fixture
def empty_title_main_soup(
    scraper: Scraper, empty_title_book_main_data_html: str
) -> BeautifulSoup:
    return scraper._get_soup(empty_title_book_main_data_html)


@pytest.fixture
def description_soup(
    scraper: Scraper, book_description_html: str
) -> BeautifulSoup:
    return scraper._get_soup(book_description_html)


@pytest.fixture
def info_table_soup(scraper: Scraper, info_table_html: str) -> BeautifulSoup:
    return scraper._get_soup(info_table_html)


@pytest.fixture
def example_book_full_html(
    book_main_data_html, book_description_html, info_table_html
) -> str:
    return f"""
    <html>
      <body>
        {book_main_data_html}
        {book_description_html}
        {info_table_html}
      </body>
    </html>
    """
