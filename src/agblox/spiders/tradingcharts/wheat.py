"""Wheat spider."""
from typing import List

from agblox.spiders.tradingcharts.tradingcharts import TradingchartsSpider


class TradingchartswheatSpider(TradingchartsSpider):
    """Spider for tradingchartswheat site."""

    name: str = "tradingchartswheat"
    url: str = "https://futures.tradingcharts.com/news/headlines/Wheat.html"
    tags: List[str] = ["wheat", "article", "tradingchartswheat"]
