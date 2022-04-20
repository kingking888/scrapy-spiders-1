"""Module for fetching financial modeling calendars."""
import logging
from typing import Iterator

from agblox.items import ModelDataItem
from agblox.settings import FRED_API_KEY, YURI
from agblox.spiders.helpers import ModelDataSpider
from fredapi import Fred
import scrapy
from scrapy.http import Request, TextResponse

log = logging.getLogger(__name__)


class FredMacroSpider(ModelDataSpider):
    """Spider for https://financialmodelingprep.com/api/v3."""

    name: str = "fred_macro"
    host_header = "fred.stlouisfed.org"
    spider_author = YURI
    s3_dir_key = "companies-models-data/macro-data/"
    file_prefix = "macro_data_"

    custom_settings = {
        "ITEM_PIPELINES": {
            "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 300,
            # "agblox.pipelines.FredMacroFSPipeline": 310,  #ToDo: Needs to be reviewed
            "agblox.pipelines.FredMacroS3Pipeline": 320,
            "agblox.pipelines.APIPipelineReport": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        }
    }

    def start_requests(self) -> Iterator[scrapy.Request]:
        """Starts from fetching tickers data."""
        yield Request("https://fred.stlouisfed.org/docs/api/fred/")

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        fred = Fred(api_key=FRED_API_KEY)
        macro_fred = [
            "ECBDFR",
            "DGS2",
            "DGS5",
            "DGS10",
            "TEDRATE",
            "M1",
            "M2",
            "WALCL",
            "WTREGEN",
            "TREAST",
            "NASDAQCOM",
            "WILL5000PRFC",
            "BAMLHYH0A0HYM2TRIV",
            "DCOILWTICO",
            "STLFSI2",
            "VXVCLS",
            "VXNCLS",
            "CCSA",
            "T5YIFR",
            "FEDFUNDS",
            "BOGMBASE",
            "TOTRESNS",
            "CURRCIR",
            "UMCSENT",
            "GEPUPPP",
            "UNRATE",
            "HOUST",
            "PAYEMS",
            "DGORDER",
            "PCE",
            "CPIAUCSL",
            "PPIACO",
            "WPS022104",
            "M1SL",
            "M2SL",
            "DEXCHUS",
            "DEXJPUS",
            "DEXUSEU",
            "DEXUSUK",
        ]
        for macro in macro_fred:
            series = fred.get_series(macro)
            data = series.to_json()
            item = ModelDataItem(data=data, ticker=macro)
            yield item
            log.info(f"Fetched macro data for {macro}")
