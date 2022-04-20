"""Agriculture.com crop market scraper."""
from typing import List

from agblox.spiders.agriculturecom.agriculturecom import AgriculturecomSpider


class AgriculturecomCropmarketSpider(AgriculturecomSpider):
    """Spider for agriculture.com crop market section."""

    name: str = "agriculturecom_crop_markets"
    url: str = "https://www.agriculture.com/markets/analysis/crops"
    tags: List[str] = ["article", "agriculturecom_crop_markets"]
