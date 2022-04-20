"""Articles spider."""
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


class SoybeansandcornSpider(BaseSpider):
    """Spider for soybeansandcorn.com site."""

    name: str = "soybeansandcorn.com"
    url: str = "http://soybeansandcorn.com/News"
    tags: List[str] = ["article", "soybeansandcorn.com"]
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//div[@id='content']//a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        # everything is in 1 page

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(
            item=ArticleItem(),
            response=response,
            date_format=[
                r"MMM[\s+]DD[.\s+]YYYY",
                r"MMM[\s+]D[.\s+]YYYY",
                r"MMMM[\s+]DD[.\s+]YYYY",
                r"MMMM[\s+]D[.\s+]YYYY",
            ],
        )

        loader.add_value("author", self.name)

        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        loader.add_xpath("created_at", "//div[@id='content']//h5/text()", TakeFirst())

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//div[@id='content']//text()")

        loader.add_xpath("title", "//div[@id='content']//h3/text()")

        loader.add_value("url", response.url)

        yield loader.load_item()
