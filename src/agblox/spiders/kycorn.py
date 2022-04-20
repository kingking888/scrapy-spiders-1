"""Corn collection spiders."""
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


class KentuckycornSpider(BaseSpider):
    """Spider for kycorn.org site."""

    name: str = "kycorn.org"
    url: str = "https://www.kycorn.org/news"
    tags: List[str] = ["corn", "article", "kycorn.org"]
    host_header = "www.kycorn.org"
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//article//a[@class='BlogList-item-title']/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        try:
            # first is newer, second is older
            next_page = etree.xpath("//a[@class='BlogList-pagination-link']/@href")[1]
        except IndexError:
            # on first page, only newer button exists
            next_page = etree.xpath("//a[@class='BlogList-pagination-link']/@href")[0]
        if "reversePaginate=true" not in next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        if not response.url.startswith("https://www.kycorn.org/news/"):
            # we aren't set up to parse redirects
            return

        loader = ItemLoader(item=ArticleItem(), response=response, date_format="YYYY-MM-DD")

        loader.add_value("author", self.name)
        loader.add_xpath(
            "created_at", "//time[@class='Blog-meta-item Blog-meta-item--date']/@datetime"
        )
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='sqs-block-content']/p/text()")
        loader.add_xpath("title", "//h1[@class='BlogItem-title']/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
