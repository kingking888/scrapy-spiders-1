"""Test suit for Yahoo finance."""
import datetime
from unittest.mock import patch

from agblox.spiders.helpers import headers
from agblox.spiders.yahoo import YahooSpider
import pytest


@pytest.fixture()
def spider():
    return YahooSpider()


headers = headers(YahooSpider.name)
headers["User-Agent"] = YahooSpider.user_agent


@pytest.mark.parametrize(
    ("ticker", "tickers", "expected"),
    [
        (
            "TRNE",
            {"TRNE": {"active": True, "date": "2020-12-04", "tags": []}},
            {
                "start": datetime.datetime(
                    2020, 12, 5, 3, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800))
                )
            },
        ),
        ("WTRH", {"WTRH": {"active": True, "date": None, "tags": []}}, {"period": "max"}),
    ],
    ids=["correct", "blank string"],
)
def test_get_period_by_ticker(spider, ticker, tickers, expected):
    assert spider.get_period_by_ticker(tickers[ticker]) == expected


@pytest.mark.parametrize(
    ("tickers", "ticker_name", "expected"),
    [
        ({"TRNE": {"active": True, "date": "2020-12-04", "tags": []}}, "TRNE", 0),
        ({"WTRH": {"active": True, "date": None, "tags": []}}, "WTRH", 1084),
        ({}, "", 0),
    ],
    ids=["ticker with date", "ticker without date", "ticker doesn't exist"],
)
def test_parse(spider, tickers, ticker_name, expected, vcr_settings):
    spider.tickers = tickers

    with vcr_settings.use_cassette(f"yahoo-finance_{ticker_name}.yaml"):
        with patch("time.time", return_value=1607433045):
            r = [e for e in spider.query_api(None)]

    assert len(r) == expected


@pytest.mark.parametrize(
    ["tickers", "ticker_name", "expected"],
    [
        (
            {"FSR": {"date": "2020-12-03"}},
            "FSR",
            [
                {
                    "close": 17.149999618530273,
                    "date": "2020-12-04T00:00:00",
                    "dividends": 0.0,
                    "high": 17.450000762939453,
                    "low": 16.65999984741211,
                    "open": 17.3799991607666,
                    "splits": 0.0,
                    "ticker": "FSR",
                    "volume": 7482200.0,
                },
                {
                    "close": 17.299999237060547,
                    "date": "2020-12-07T00:00:00",
                    "dividends": 0.0,
                    "high": 18.139999389648438,
                    "low": 16.8799991607666,
                    "open": 17.84000015258789,
                    "splits": 0.0,
                    "ticker": "FSR",
                    "volume": 10974700.0,
                },
            ],
        ),
    ],
)
def test_parse_correct_item(spider, vcr_settings, tickers, ticker_name, expected):
    spider.tickers = tickers

    with vcr_settings.use_cassette(f"yahoo-finance_{ticker_name}.yaml"):
        with patch("time.time", return_value=1607433045):
            r = [e for e in spider.query_api(None)]

    assert r == expected
