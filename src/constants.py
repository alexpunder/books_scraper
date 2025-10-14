from pathlib import Path


BASE_DIR = Path(__file__).parent.parent

BOOKS_DATA_FILENAME = "books_data.txt"
SAVE_DIR_PATH = BASE_DIR / "artifacts"
FILE_PATH = SAVE_DIR_PATH / BOOKS_DATA_FILENAME

BASE_URL: str = "https://books.toscrape.com/catalogue/"
START_CATALOGUE_PAGE_URL: str = BASE_URL + "page-1.html"

CLEAN_CURRENCY: str = "Â"
RESPONSE_TIMEOUT: int = 10

EMPTY_DATA: str = "Нет данных"
LINK_NOT_FOUND: str = "Ссылка перехода отсутствует"
UNKNOWN_RATING: str = "Unknown"
UNKNOWN_RATING_VALUE: str = "Неизвестное значение"

RATING_MAP: dict[str, str] = {
    "One": "1",
    "Two": "2",
    "Three": "3",
    "Four": "4",
    "Five": "5",
    UNKNOWN_RATING: UNKNOWN_RATING_VALUE,
}

TASK_START_TIME: str = "19:00"
DELAY: int = 10
