"""BabyPips articles spider."""
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


class BabyPipsSpider(BaseSpider):
    """Spider for babypips.com site."""

    name: str = "babypips.com"
    url: str = "https://www.babypips.com/news"
    tags: List[str] = ["Forex", "article", "babypips.com"]
    host_header = "www.babypips.com"
    spider_author = DANIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//a[@class='read-more']/@href"):
            if self.last_url and article in self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        next_page = etree.xpath("//a[@class='pager' and @rel='next']/@href")
        if next_page:
            yield scrapy.Request(next_page[0], callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", "//meta[@property='article:published_time']/@content")

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//div[@class='post-content article-content']//p//text()")

        loader.add_xpath("title", "//h1[@class='headline']/text()")

        loader.add_value("url", response.url)

        yield loader.load_item()
