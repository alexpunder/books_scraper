from dataclasses import dataclass, field
from typing import Any

from constants import (
    BACKOFF_FACTOR,
    BASE_URL,
    CLEAN_CURRENCY,
    DEFAULT_HEADERS,
    EMPTY_DATA,
    FILE_PATH,
    LINK_NOT_FOUND,
    MAX_RETRIES,
    RATING_MAP,
    RESPONSE_TIMEOUT,
    RETRY_STATUSES,
    SAVE_DIR_PATH,
    START_CATALOGUE_PAGE_URL,
    TASK_START_TIME,
    UNKNOWN_RATING,
    UNKNOWN_RATING_VALUE,
)


@dataclass
class SessionConfig:
    """Конфигурация для HTTP сессии"""

    max_retries: int | None = MAX_RETRIES
    backoff_factor: float | None = BACKOFF_FACTOR
    retry_statuses: tuple[int] | None = RETRY_STATUSES
    default_headers: dict[str, Any] = field(
        default_factory=lambda: DEFAULT_HEADERS.copy()
    )


@dataclass
class ScraperConfig:
    """Конфигурация для скрапера"""

    base_url: str = BASE_URL
    start_catalog_page: str = START_CATALOGUE_PAGE_URL

    response_timeout: int | None = RESPONSE_TIMEOUT

    file_path: str = FILE_PATH
    save_dir_path: str = SAVE_DIR_PATH

    start_time: str = TASK_START_TIME

    clean_currency: str = CLEAN_CURRENCY
    empty_data: str = EMPTY_DATA
    link_not_found: str = LINK_NOT_FOUND
    unknown_rating: str = UNKNOWN_RATING
    unknown_rating_value: str = UNKNOWN_RATING_VALUE
    rating_map: dict[str, Any] = field(
        default_factory=lambda: RATING_MAP.copy()
    )


session_conf: SessionConfig = SessionConfig()
scraper_conf: ScraperConfig = ScraperConfig()
