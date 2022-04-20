"""Gizmodo Spider."""

import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import AZKA
from agblox.spiders.helpers import BaseSpider
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class GizmodoSpider(BaseSpider):
    """Spider for gizmodo.com site."""

    name: str = "gizmodo.com"
    url: str = "https://gizmodo.com/latest"
    tags: List[str] = ["article", "gizmodo.com"]
    host_header = "gizmodo.com"
    spider_author = AZKA

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse Navigation page."""
        for article in response.xpath("//div[@class='sc-3kpz0l-7 ibQcju']/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield response.follow(article.get(), callback=self.parse_article)

        next_page = response.xpath("//div[@class='sc-1uzyw0z-0 kNHeFZ']/a/@href").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Parsing: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)
        loader.add_xpath("created_at", "//time/@datetime")
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='js_starterpost']/div/p/text()")
        loader.add_xpath("title", "//h1/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
