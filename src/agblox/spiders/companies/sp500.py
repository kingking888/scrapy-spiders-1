"""Module that using for obtain S&P500 companies tickers list from zacks.com."""

import logging
import re
from typing import Iterator

from agblox.items import ModelDataItem
from agblox.settings import YURI
from agblox.spiders.helpers import ModelDataSpider
import requests
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class SP500Spider(ModelDataSpider):
    """Spider for https://www.zacks.com/funds/etf/."""

    host_header = "www.zacks.com"
    spider_author = YURI
    name = "zacks_sp500"
    s3_dir_key = "companies-models-data/tickers/"
    file_prefix = "tickers_"
    custom_settings = {
        "ITEM_PIPELINES": {
            "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 300,
            "agblox.pipelines.FSModelDataPipeline": 310,
            "agblox.pipelines.S3ModelSP500Pipeline": 320,
            "agblox.pipelines.APIPipelineReport": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        }
    }

    sector_indexes = {
        "Communication Services": "XLC",
        "Consumer Discretionary": "XLY",
        "Consumer Staples": "XLP",
        "Energy": "XLE",
        "Financials": "XLF",
        "Health Care": "XLV",
        "Industrials": "XLI",
        "Materials": "XLB",
        "Real Estate": "XLRE",
        "Technology": "XLK",
        "Utilities": "XLU",
        "S&P500": "SPY",
    }

    @staticmethod
    def create_url(index: str) -> str:
        """Override to return holding for specific index.

        Args:
            index: sector index
        Return:
            Link for specific index
        """
        return f"https://www.zacks.com/funds/etf/{index}/holding"

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping.

        Method uses scrapy.Request just for starting. All job will be done by requests.
        Reason: zacks.com blocks scrapy bot with 500 Internal Server Error
        """
        keys = list(self.sector_indexes.values())
        indexes = dict.fromkeys(keys)

        yield scrapy.Request(
            url="https://www.zacks.com/",
            callback=self.parse,
            cb_kwargs={"indexes": indexes, "keys": keys},
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
            },
        )

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        loader = ItemLoader(item=ModelDataItem(), response=response)
        for key in response.cb_kwargs["keys"]:
            url = self.create_url(key)
            req = requests.Session()
            req.headers.update(response.request.headers)
            r = req.get(url)
            goal = re.findall(r"etf\\/(.*?)\\", r.text)
            indexes = kwargs.get("indexes")
            indexes[key] = goal
            # if None not in indexes.values():
            loader.add_value("data", indexes)
            log.info("Loaded tickers for sector: %s" % key)
        yield loader.load_item()
        log.info("Collected all tickers for S&P500 companies, divided by sector")
