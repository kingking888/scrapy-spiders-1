"""Corn spider."""
from typing import List

from agblox.spiders.tradingcharts.tradingcharts import TradingchartsSpider


class TradingchartscornSpider(TradingchartsSpider):
    """Spider for tradingchartscorn site."""

    name: str = "tradingchartscorn"
    url: str = "https://futures.tradingcharts.com/news/headlines/Corn.html"
    tags: List[str] = ["corn", "article", "tradingchartscorn"]
