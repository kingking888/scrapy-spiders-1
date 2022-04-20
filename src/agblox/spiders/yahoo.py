"""Yahoo stock market spider."""
import datetime
import logging
from typing import Any, Dict, Iterator, Union

from agblox.items import TickerItem
from agblox.settings import ARKADY
from agblox.spiders.helpers import BaseSpider
import scrapy
from scrapy.http import TextResponse
import yfinance as yf

log = logging.getLogger(__name__)


class YahooSpider(BaseSpider):
    """Spider for yahoo finance stock market.

    This spider don't store raw data, bcoz we don't expect ambiguity in the API responses.
    """

    name = "yahoo-finance"
    host_header = "finance.yahoo.com"
    tickers: Dict[str, Any] = None
    spider_author = ARKADY

    custom_settings = {
        "ITEM_PIPELINES": {
            "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 300,
            "agblox.pipelines.APIPipeline": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        }
    }

    def more_than_now(self, date: datetime.datetime) -> bool:
        """That is helper which check that input date more than now."""
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        return date > now

    def start_requests(self) -> None:
        """This method is called by Scrapy when the spider is opened for scraping.

        In this scrapper we use yfinance for work whit yahoo finance API.
        This method just placeholder.
        """
        self.tickers = self.get_cfg()
        yield scrapy.Request(url="https://finance.yahoo.com", callback=self.query_api)

    def get_period_by_ticker(
        self, cfg: dict
    ) -> Union[Dict[str, datetime.datetime], Dict[str, str]]:
        """This method extract the period for history data."""
        last = cfg["date"]
        if last is None:
            return {"period": "max"}
        # Fix for yfinance. Lib trying to use server timezone and it can break tests.
        v = datetime.datetime.strptime(last, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
        # Will start next day after existing
        v += datetime.timedelta(days=1)
        return {"start": v.astimezone()}

    def query_api(
        self,
        _response: TextResponse,
    ) -> Iterator[TickerItem]:
        """Read data from Yahoo."""
        for ticker, cfg in self.tickers.items():
            data = yf.Ticker(ticker)
            period = self.get_period_by_ticker(cfg)
            if period.get("start") and self.more_than_now(period["start"]):
                continue
            log.info(f"Ticker: {ticker}, {period}")
            for timestamp, row in data.history(**period).iterrows():
                item = TickerItem()
                item["close"] = row["Close"]
                item["date"] = timestamp.isoformat()
                item["dividends"] = row["Dividends"]
                item["high"] = row["High"]
                item["low"] = row["Low"]
                item["open"] = row["Open"]
                item["splits"] = row["Stock Splits"]
                item["ticker"] = ticker
                item["volume"] = row["Volume"]
                yield item
