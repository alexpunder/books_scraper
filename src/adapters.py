import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import SessionConfig, session_conf


class HttpClientManager:
    """
    Менеджер для управления HTTP-сессиями с настройкой повторных попыток и заголовков.

    Обеспечивает ленивую инициализацию сессии и централизованную конфигурацию
    параметров HTTP-соединения, включая повторные попытки и заголовки по умолчанию.

    Attributes:
        _session (requests.Session | None): HTTP-сессия, инициализируемая при первом обращении
        _config (SessionConfig): Конфигурация параметров сессии
    """

    def __init__(self, config: "SessionConfig") -> None:
        self._session: "requests.Session" | None = None
        self._config: "SessionConfig" = config

    @property
    def session(self) -> requests.Session:
        """
        Инициализирует менеджер HTTP-клиента.

        Args:
            config: Конфигурация параметров сессии, включая заголовки,
                   настройки повторных попыток и другие параметры
        """
        if not self._session:
            self._session = requests.Session()
            self._configure_session()
        return self._session

    def _configure_session(self) -> None:
        """
        HTTP-сессия с примененной конфигурацией.

        Сессия инициализируется лениво при первом обращении к свойству
        и настраивается в соответствии с переданной конфигурацией.

        Returns:
            Настроенный экземпляр requests.Session

        Note:
            Последующие вызовы возвращают один и тот же экземпляр сессии
        """
        if self._config.default_headers:
            self._session.headers.update(self._config.default_headers)

        retry_strategy = Retry(
            total=self._config.max_retries,
            backoff_factor=self._config.backoff_factor,
            status_forcelist=self._config.retry_statuses,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)


scraper_http_manager: "HttpClientManager" = HttpClientManager(session_conf)
