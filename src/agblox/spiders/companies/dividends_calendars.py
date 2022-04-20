"""Module for fetching financial modeling calendars."""
import logging
from typing import Iterator

from agblox.items import ModelDataItem
from agblox.settings import DANIYAL, FINANCIAL_MODELING_PREP_API_KEY
from agblox.spiders.helpers import ModelDataSpider
import scrapy
from scrapy.http import Request, TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class DividendsCalendarsSpider(ModelDataSpider):
    """Spider for https://financialmodelingprep.com/api/v3."""

    name: str = "dividends_calendars"
    api_url: str = "https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend"
    download_delay = 0.30
    spider_author = DANIYAL
    host_header = "financialmodelingprep.com"
    s3_dir_key = "companies-models-data/dividends/"
    file_prefix = "dividends_ca_"

    custom_settings = {
        "ITEM_PIPELINES": {
            "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 300,
            "agblox.pipelines.FinCalendarsPipeline": 310,
            "agblox.pipelines.S3ModelCalendarsPipeline": 320,
            "agblox.pipelines.APIPipelineReport": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        }
    }

    def build_url(self, ticker: str) -> str:
        """Helper method for creating url."""
        return f"{self.api_url}/{ticker}?limit=20&apikey={FINANCIAL_MODELING_PREP_API_KEY}"

    def start_requests(self) -> Iterator[scrapy.Request]:
        """Starts from fetching tickers data."""
        tickers500 = self.fetch_tickers_from_s3()
        spy = tickers500[0]["SPY"]
        for ticker in spy:
            url = self.build_url(ticker)
            yield Request(url, cb_kwargs={"ticker": ticker})

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        loader = ItemLoader(item=ModelDataItem(), response=response)
        loader.add_value("data", response.body)
        loader.add_value("ticker", kwargs.get("ticker"))
        self.logger.info("Processed ticker: %s" % kwargs.get("ticker"))
        yield loader.load_item()
