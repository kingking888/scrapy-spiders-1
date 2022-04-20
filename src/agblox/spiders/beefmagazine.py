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


class BeefMagazineSpider(BaseSpider):
    """Spider for beefmagazine.com site."""

    name: str = "beefmagazine.com"
    url: str = "https://www.beefmagazine.com/livestock?infscr=1"
    tags: List[str] = ["slaughter cattle", "article", "beefmagazine.com"]
    host_header = "www.beefmagazine.com"
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//div[@class='title']/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = etree.xpath("//a[@rel='next']/@href")[0]
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)
        loader.add_xpath("created_at", "//meta[@itemprop='dateModified']/@content")
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='article-content ']//text()")
        loader.add_xpath("title", "//h1[@itemprop='headline']/text()")
        loader.add_value("url", response.url)
        yield loader.load_item()
