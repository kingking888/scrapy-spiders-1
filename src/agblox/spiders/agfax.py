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


class AgfaxSpider(BaseSpider):
    """Spider for agfax.com site."""

    name: str = "agfax.com"
    url: str = "https://agfax.com/tag/corn-news/"
    tags: List[str] = ["article", "agfax.com"]
    spider_author = DANIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//div[@class='article-big featured']/h2/a/@href"):
            if article.startswith("https://agfax.com/"):  # skip advertisements
                if article == self.last_url:
                    log.info("Limit reached.")
                    return
                yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = etree.xpath("//a[contains(text(),'Older posts')]/@href")[0]
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", "//time[@class='entry-date published updated']/@datetime")
        loader.add_xpath("created_at", "//time[@class='entry-date published']/@datetime")

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='entry-content']/p//text()")
        loader.add_xpath("title", "//h1[@class='entry-title']/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
