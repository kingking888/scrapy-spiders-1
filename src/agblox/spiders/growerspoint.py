"""Articles spider."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import DANIEL
from agblox.spiders.helpers import BaseSpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class GrowerspointSpider(BaseSpider):
    """Spider for growerspoint.com site."""

    name: str = "growerspoint.com"
    url: str = "https://growerspoint.com/category/crops/wheat/page/1/"
    tags: List[str] = ["article", "growerspoint.com"]
    host_header = "growerspoint.com"
    spider_author = DANIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//h3[@class='entry-title td-module-title']/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        next_page = etree.xpath("//i[@class='td-icon-menu-right']/parent::*/@href")
        if next_page:
            yield scrapy.Request(next_page[0], callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)

        loader.add_xpath(
            "created_at", "//time[@class='entry-date updated td-module-date']/@datetime"
        )

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//div[@class='td-post-content']//text()")

        loader.add_xpath("title", "//h1[@class='entry-title']/text()")

        loader.add_value("url", response.url)

        yield loader.load_item()
