"""Slaughter Cattle collection spiders."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import ARKADY
from agblox.spiders.helpers import BaseSpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class TheBeefReadSpider(BaseSpider):
    """Spider for thebeefread.com site."""

    name: str = "thebeefread.com"
    url: str = "http://www.thebeefread.com"
    tags: List[str] = ["slaughter cattle", "article", "thebeefread.com"]
    host_header = "www.thebeefread.com"
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath(
            "//header[@class='entry-header']/h2[@class='entry-title']/a/@href"
        ):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = str(etree.xpath("//a[contains(text(),'→')]/@href")[0])
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", "//p[@class='p-meta']/span/time/@datetime")

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//div[@class='entry-content content']//text()")
        loader.add_xpath("title", "//h1[@class='entry-title']/text()")

        loader.add_value("url", response.url)

        yield loader.load_item()
