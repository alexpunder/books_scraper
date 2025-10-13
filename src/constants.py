from pathlib import Path


BASE_DIR = Path(__file__).parent.parent

BOOKS_DATA_FILENAME = "books_data.txt"
SAVE_DIR_PATH = BASE_DIR / "artifacts"
FILE_PATH = SAVE_DIR_PATH / BOOKS_DATA_FILENAME

BASE_URL: str = "https://books.toscrape.com/catalogue/"

# TODO: вернуть номер страницы на 1
START_CATALOGUE_PAGE_URL: str = BASE_URL + "page-50.html"

CLEAN_CURRENCY: str = "Â"

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

# TODO: вернуть время на 19:00
TASK_START_TIME:str = "16:15"
WAITING_TIME: int = 10
RESPONSE_TIMEOUT: int = 10
