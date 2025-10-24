import random
import threading
from abc import ABC, abstractmethod
from typing import NewType
from pydantic import AnyHttpUrl, ValidationError


LongUrl = NewType("LongUrl", str)
ShortUrl = NewType("ShortUrl", str)


DEFAULT_DOMAIN: str = "https://rev.me"
DEFAULT_LIMIT: int = 100
DEFAULT_POOL: list[str] = [
    f"pool{idx}"
    for idx in range(DEFAULT_LIMIT)
]


class InvalidLinkError(Exception): ...


class LimitReachedError(Exception): ...


class UnknownUrlError(Exception): ...


class Strategy(ABC):

    @abstractmethod
    def generate(self) -> str:
        raise NotImplementedError


class IncrementalStrategy(Strategy):
    def __init__(self) -> None:
        self.counter = 1

    def generate(self) -> str:
        result = self.counter
        self.counter += 1
        return str(result)


class FromPoolStrategy(Strategy):
    def __init__(self, pool: list[str]) -> None:
        self.pool = pool

    def generate(self) -> str:
        option = random.choice(self.pool)
        self.pool.remove(option)
        return option


class Shortener:

    def __init__(
        self,
        shorten_strategy: Strategy,
        default_domain: str = DEFAULT_DOMAIN,
        default_limit: int = DEFAULT_LIMIT,
    ) -> None:
        self.default_domain = default_domain
        self.shorten_strategy = shorten_strategy
        self.default_limit = default_limit

        self._short_link_to_long_link_map: dict[ShortUrl, LongUrl] = {}
        self._long_link_to_short_link_map: dict[LongUrl, ShortUrl] = {}
        self.__lock = threading.Lock()

    def shorten(self, url: LongUrl) -> ShortUrl:
        if url in self._long_link_to_short_link_map:
            return self._long_link_to_short_link_map[url]

        with self.__lock:

            if self._storage_limit_reached():
                raise LimitReachedError

            if not self.is_url_valid(url):
                raise InvalidLinkError

            identification = self.shorten_strategy.generate()
            shorten_url = ShortUrl(f"{self.default_domain}/{identification}")

            self._short_link_to_long_link_map[shorten_url] = url
            self._long_link_to_short_link_map[url] = shorten_url

            return shorten_url

    def get(self, url: ShortUrl) -> LongUrl:
        result = self._short_link_to_long_link_map.get(url)
        if not result:
            raise UnknownUrlError

        return result

    def _storage_limit_reached(self) -> bool:
        return len(self._short_link_to_long_link_map) >= self.default_limit

    @staticmethod
    def is_url_valid(url: LongUrl) -> bool:
        try:
            AnyHttpUrl(url)
            return True
        except ValidationError:
            return False