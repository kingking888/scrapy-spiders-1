"""Agriculture.com corn scraper."""
from typing import List

from agblox.spiders.agriculturecom.agriculturecom import AgriculturecomSpider


class AgriculturecomWheatSpider(AgriculturecomSpider):
    """Spider for agriculture.com wheat section."""

    name: str = "agriculturecom_wheat"
    url: str = "https://www.agriculture.com/crops/wheat"
    tags: List[str] = ["wheat", "article", "agriculturecom_wheat"]
