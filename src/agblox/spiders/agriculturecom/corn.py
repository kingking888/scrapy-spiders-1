"""Agriculture.com corn scraper."""
from typing import List

from agblox.spiders.agriculturecom.agriculturecom import AgriculturecomSpider


class AgriculturecomCornSpider(AgriculturecomSpider):
    """Spider for agriculture.com corn section."""

    name: str = "agriculturecom_corn"
    url: str = "https://www.agriculture.com/crops/corn"
    tags: List[str] = ["corn", "article", "agriculturecom_corn"]
