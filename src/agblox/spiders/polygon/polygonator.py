"""Spider that uses polygon API for collecting the data."""
from abc import ABC
import datetime
from typing import Dict, Iterator

from agblox.items import PolygonStockAggregatedItem
from agblox.settings import YURI
from agblox.spiders.helpers import PolygonSpider
import scrapy
from scrapy.loader import ItemLoader


class Polygonator(PolygonSpider, ABC):
    """Common spider class for Polygon API."""

    name = "polygonator"
    spider_author = YURI
    host_header = "api.polygon.io"
    download_delay = 0.2
    custom_settings = {
        "ITEM_PIPELINES": {
            "agblox.pipelines.CSVPipeline": 310,
            # "agblox.pipelines.S3CSVPipeline": 320,
            "agblox.pipelines.S3CSVDailyAggPipeline": 320,
            "agblox.pipelines.APIPipelineReport": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        },
        # "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        # "CONCURRENT_ITEMS": 100000
    }
    csv_filename = "stocks_daily_bars"
    csv_fieldnames = ["ticker", "c", "h", "l", "n", "o", "t", "v", "vw"]

    def start_requests(self) -> Iterator[scrapy.Request]:
        """Initiate client and make a dummy request just for scrapy start.

        It's a placeholder method
        """
        resp = self.get_tickers_from_api(500, "volume")
        tickers_conf = self._convert_to_config(resp)
        for ticker in tickers_conf:
            from_date = ticker[1] if ticker[1] else "2000-01-01"
            to_date = datetime.date.today()
            url = (
                f"https://api.polygon.io/v2/aggs/ticker/"
                f"{ticker[0]}/range/1/day/{from_date}/{to_date}"
                f"?adjusted=true&sort=desc&limit=50000&apiKey={self.key}"
            )
            yield scrapy.Request(url, cb_kwargs={"ticker": ticker[0]})

    def parse(self, response: scrapy.http.HtmlResponse, **kwargs) -> Iterator:
        """Method for parsing.

        Will be called for each response.
        """
        data = response.json()
        self.logger.info("Received data for: %s" % kwargs.get("ticker"))
        yield self.add_item(data.get("results"), kwargs.get("ticker"))

    @staticmethod
    def _convert_to_config(resp: Dict) -> Iterator:
        """Combine configuration for our spider."""
        return [(x["ticker"], None) for x in resp]

    @staticmethod
    def add_item(result: Dict, ticker: str) -> ItemLoader:
        """Adding each item to the loader."""
        loader = ItemLoader(item=PolygonStockAggregatedItem())
        loader.add_value("ticker", ticker)
        loader.add_value("result", result)
        return loader.load_item()
