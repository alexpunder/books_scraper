from pathlib import Path
from typing import Any

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
TIMEOUT: int | None = 30
MAX_RETRIES: int | None = 3
BACKOFF_FACTOR: float | None = 0.5
RETRY_STATUSES: tuple[int] | None = (500, 502, 503, 504)
DEFAULT_HEADERS: dict[str, Any] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
