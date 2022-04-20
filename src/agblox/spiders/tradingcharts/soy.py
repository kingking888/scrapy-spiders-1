"""Soy spider."""
from typing import List

from agblox.spiders.tradingcharts.tradingcharts import TradingchartsSpider


class TradingchartssoySpider(TradingchartsSpider):
    """Spider for trading charts soy site."""

    name: str = "tradingchartssoy"
    url: str = "https://futures.tradingcharts.com/news/headlines/Soybeans.html"
    tags: List[str] = ["soy", "article", "tradingchartssoy"]
