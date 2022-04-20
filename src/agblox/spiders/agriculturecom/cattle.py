"""Agriculture.com cattle scraper."""
from typing import List

from agblox.spiders.agriculturecom.agriculturecom import AgriculturecomSpider


class AgriculturecomCattleSpider(AgriculturecomSpider):
    """Spider for agriculture.com cattle section."""

    name: str = "agriculturecom_cattle"
    url: str = "https://www.agriculture.com/livestock/cattle"
    tags: List[str] = ["article", "agriculturecom_cattle"]
