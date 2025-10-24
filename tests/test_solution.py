import random

import pytest

from src.solution import (
    Shortener,
    DEFAULT_DOMAIN,
    DEFAULT_LIMIT,
    LongUrl,
    ShortUrl,
    InvalidLinkError,
    LimitReachedError,
    UnknownUrlError,
    IncrementalStrategy,
    FromPoolStrategy,
    DEFAULT_POOL,
)


class TestShortener:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.shortener = Shortener(
            shorten_strategy=IncrementalStrategy()
        )

    def test_service_should_pick_random_value_from_pool_and_generate_short_url(self) -> None:
        # Given
        random.seed(42)
        self.shortener.shorten_strategy = FromPoolStrategy(
            pool=DEFAULT_POOL
        )
        sample_url = LongUrl("https://google.com")
        # When
        short_link = self.shortener.shorten(
            sample_url
        )
        # Then
        assert short_link == f"{DEFAULT_DOMAIN}/pool81"

    def test_service_should_return_expected_short_url(self) -> None:
        # Given
        sample_url = LongUrl("https://google.com")
        short_link = self.shortener.shorten(
            sample_url
        )
        # When
        result = self.shortener.get(
            short_link
        )
        # Then
        assert result == sample_url

    def test_service_should_raise_when_unknown_url_is_passed(self) -> None:
        # When/Then
        with pytest.raises(UnknownUrlError):
            self.shortener.get(
                ShortUrl("https://rev.me")
            )

    def test_service_should_shorten_the_long_url(self) -> None:
        # Given
        sample_url = LongUrl("https://google.com")
        # When
        result = self.shortener.shorten(
            sample_url
        )
        # Then
        assert result == f"{DEFAULT_DOMAIN}/1"

    def test_service_should_return_same_short_link_idempotently(self):
        # Given
        sample_url = LongUrl("https://google.com")
        # When/Then
        assert self.shortener.shorten(sample_url) == self.shortener.shorten(sample_url)

    @pytest.mark.parametrize(
        "invalid_url",
        [
            "",
            "sdafdfasd",
            None,
        ]
    )
    def test_service_should_raise_when_invalid_url_is_provided(
        self,
        invalid_url: str,
    ) -> None:
        # When/Then
        with pytest.raises(InvalidLinkError):
            self.shortener.shorten(invalid_url)  # type: ignore

    def test_service_should_not_store_more_links_than_the_limit(self) -> None:
        # Given
        for idx in range(DEFAULT_LIMIT):
            self.shortener.shorten(
                LongUrl(f"https://google.com/{idx}")
            )
        # When/Then
        with pytest.raises(LimitReachedError):
            self.shortener.shorten(
                LongUrl("https://google.com/new")
            )

    def test_service_should_return_same_link(self) -> None:
        # Given
        for idx in range(DEFAULT_LIMIT):
            self.shortener.shorten(
                LongUrl(f"https://google.com/{idx}")
            )
        # When/Then
        self.shortener.shorten(
            LongUrl("https://google.com/99")
        )
