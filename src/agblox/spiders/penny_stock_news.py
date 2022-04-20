"""Penny Stock News Spider."""

import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import ROSS
from agblox.spiders.helpers import BaseSpider
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from scrapy.settings import Settings

log = logging.getLogger(__name__)


class PennyStockNewsSpider(BaseSpider):
    """Spider for pennystock.news site."""

    name: str = "pennystock.news"
    url: str = "https://pennystocks.news/category/uncategorized/"
    tags: List[str] = ["article", "pennystock.news", "equity"]
    host_header = "pennystock.news"
    handle_httpstatus_list = [401, 501]

    headers = {
        "authority": "penny_stocks.news",
        "method": "GET",
        "path": "/category/uncategorized/page/2/",
    }
    spider_author = ROSS

    @classmethod
    def update_settings(cls, settings: Settings) -> None:
        """Customize spider settings."""
        cls.custom_settings["DEFAULT_REQUEST_HEADERS"] = cls.headers
        settings.setdict(cls.custom_settings or {}, priority="spider")

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse Navigation page."""
        for link in response.xpath("//h3[@class='entry-title']/a/@href"):
            if link == self.last_url:
                log.info("Limit reached.")
                return
            yield response.follow(link.get(), callback=self.parse_article)

        next_page = response.xpath("//a[@class='page-numbers nav-next']/@href").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.spider_author)
        loader.add_xpath("created_at", "//meta[@property='article:published_time']/@content")
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_value("text", response.xpath("//article").extract())

        value = response.xpath("//h1[@class='entry-title']/text()").extract()
        if len(value) > 0:
            loader.add_value("title", str(value[0]))
        else:
            """In this case drop the item because otherwise
            validation will failed due to field too short i.e.; ''"""
            return
        loader.add_value("url", response.url)

        yield loader.load_item()
