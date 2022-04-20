"""Module for fetching yahoo finance stock mart companies."""
from datetime import datetime
import logging
from typing import Dict, Iterator, List

from agblox.items import ModelDataItem
from agblox.settings import DANIYAL
from agblox.spiders.helpers import ModelDataSpider
import pandas as pd
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
import yfinance as yf

log = logging.getLogger(__name__)


class YahooCompaniesSpider(ModelDataSpider):
    """Spider for yahoo finance stock market companies."""

    name = "yahoo_companies"
    host_header = "finance.yahoo.com"
    spider_author = DANIYAL
    custom_settings = {
        "ITEM_PIPELINES": {
            "agblox.pipelines.FSJsonPipeline": 310,
            "agblox.pipelines.S3JsonPipeline": 320,
            "agblox.pipelines.APIPipelineReport": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        }
    }

    def start_requests(self) -> None:
        """This method is called by Scrapy when the spider is opened for scraping.

        In this scrapper we use yfinance to work with yahoo finance API.
        This method is just placeholder.
        """
        yield scrapy.Request(url="https://finance.yahoo.com", callback=self.query_api)

    def query_api(self, response: TextResponse) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        file_prefixes = ["price", "price_sector", "volume", "macro_yahoo"]
        tickers = self.fetch_tickers_from_s3()
        tickers500 = tickers[0]["SPY"]

        # Time Interval
        start = datetime(2008, 1, 1)
        end = datetime.today()

        for prefix in file_prefixes:
            if prefix in ["price", "volume"]:
                for ticker in tickers500:
                    self.file_prefix = f"{ticker}"
                    self.s3_dir_key = f"{prefix}/{ticker}"
                    data = self.get_data(prefix, start, end, ticker)
                    loader = ItemLoader(item=ModelDataItem(), response=response)
                    loader.add_value("data", data)
                    yield loader.load_item()
            else:
                self.file_prefix = prefix
                self.s3_dir_key = f'{prefix.replace("_", "-")}'
                data = self.get_data(prefix, start, end, tickers500)
                loader = ItemLoader(item=ModelDataItem(), response=response)
                loader.add_value("data", data)
                yield loader.load_item()

    def get_data(self, data_type: str, *args) -> callable:
        """Dispatcher for data types retrieval from Yahoo-finance."""
        func_map = {
            "price": self.get_price,
            "price_sector": self.get_price_sector,
            "volume": self.get_volume,
            "macro_yahoo": self.get_macro,
        }
        return func_map[data_type](*args)

    def get_price(self, start: datetime, end: datetime, ticker: str) -> Dict:
        """Fucntion will return price for the given time interval."""
        price = yf.Ticker(ticker).history(start=start, end=end)[["Close"]]
        price.reset_index(inplace=True)
        price_data = price.to_json(orient="records")
        log.info("Collected prices data for ticker: %s" % ticker)
        return price_data

    def get_price_sector(self, start: datetime, end: datetime, tickers: List) -> Dict:
        """Function will return price sector for the given time interval."""
        sector_tiks = {
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
        }
        # sector etfs prices
        price_sector = yf.Tickers(" ".join(list(sector_tiks.values()))).history(
            start=start, end=end
        )[["Close"]]
        price_sector.columns = price_sector.columns.droplevel()
        price_sector.reset_index(inplace=True)
        price_sector_data = price_sector.to_json(orient="records")
        log.info("Collected prices for sectors")
        return price_sector_data

    def get_macro(self, start: datetime, end: datetime, tickers: List) -> Dict:
        """Function will return macro for the given time interval."""
        macroeconomic_variables = [
            "CNYUSD=X",
            "^BVSP",
            "EURUSD=X",
            "^DJI",
            "^RUA",
            "^N225",
            "^VIX",
            "GC=F",
            "BTC-USD",
            "^GSPC",
            "^FCHI",
            "JPY=X",
            "DAX",
            "^HSI",
            "GBPUSD=X",
            "DX-Y.NYB",
            "^W5000",
            "CL=F",
            "FANG.L",
            "^CMC200",
            "^FTSE",
            "SI=F",
            "NG=F",
        ]
        yfin = yf.Tickers(" ".join(macroeconomic_variables)).history(start=start, end=end)[
            ["Close"]
        ]
        yfin.columns = yfin.columns.droplevel()
        yfin.reset_index(inplace=True)
        yfin_data = yfin.to_json(orient="records")
        log.info("Collected macro data")
        return yfin_data

    def get_volume(self, start: datetime, end: datetime, ticker: str) -> Dict:
        """Function will return volume for the given time interval."""
        volume = yf.Ticker(ticker).history(start=start, end=end)[["Volume"]]
        volume.reset_index(inplace=True)
        volume_data = volume.to_json(orient="records")
        log.info("Collected volumes data for ticker: %s" % ticker)
        return volume_data

    def _df_to_dict(self, dataframe: pd.DataFrame) -> Dict:
        """Function will convert dataframe to dict."""
        dataframe = dataframe.reset_index()
        return dataframe.to_dict(orient="records")
