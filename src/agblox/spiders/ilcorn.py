"""Corn collection spiders."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import ARKADY
from agblox.spiders.helpers import BaseSpider
from itemloaders.processors import TakeFirst
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class IlcornSpider(BaseSpider):
    """Spider for ilcorn.org site."""

    name: str = "ilcorn.org"
    url: str = "https://www.ilcorn.org/news-and-media/current-news"
    tags: List[str] = ["article", "ilcorn.org"]
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//a[@class='amsd-more-link cms-btn']/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        # unless you manually scrape through archive there's only 1 page

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MMM DD, YYYY")

        loader.add_value("author", self.name)
        loader.add_xpath(
            "created_at",
            "//p[@class='amsd-subtitle-text meta-info profile-page']/text()",
            TakeFirst(),
        )
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='profile-text-wrapper']/p/text()")
        loader.add_xpath("title", "//h1[@class='interiors title']/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
