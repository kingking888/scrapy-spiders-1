"""Agriculture.com soy scraper."""
from typing import List

from agblox.spiders.agriculturecom.agriculturecom import AgriculturecomSpider


class AgriculturecomSoybeansSpider(AgriculturecomSpider):
    """Spider for agriculture.com soybean section."""

    name: str = "agriculturecom_soy"
    url: str = "https://www.agriculture.com/crops/soybeans"
    tags: List[str] = ["article", "agriculturecom_soy", "soy"]
