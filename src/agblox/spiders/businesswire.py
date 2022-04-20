"""BusinessWire collection spiders."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import AZKA
from agblox.spiders.helpers import BaseSpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from twisted.internet.error import TimeoutError

log = logging.getLogger(__name__)


class BusinessWireSpider(BaseSpider):
    """Spider for businesswire.com site."""

    name: str = "businesswire.com"
    url: str = "https://www.businesswire.com/portal/site/home/news/"
    tags: List[str] = ["businesswire", "article", "equity"]
    host_header = "www.businesswire.com"
    page = 1
    spider_author = AZKA
    download_delay = 0.30

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//li/div[@itemscope='itemscope']/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article, errback=self.handle_error)
        try:
            next_page = etree.xpath("//div[@class='pagingNext']/a/@href")[0]
        except IndexError:
            return
        yield scrapy.Request(url=next_page, callback=self.parse, errback=self.handle_error)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)
        date = response.xpath("//div[@class='bw-release-timestamp']/time/@datetime").get()
        if not date:
            error = response.xpath("//div[@class='error-body']/h1/text()").get()
            log.info(f"For URL '{response.url}', {error}")
            return
        loader.add_value("created_at", str(date))
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='bw-release-story']//p/text()")
        loader.add_xpath("title", "//meta[@itemprop='headline']/@content")
        loader.add_value("url", response.url)

        yield loader.load_item()

    def handle_error(self, failure: object) -> None:
        """Handle errors with log warning."""
        if failure.check(TimeoutError):
            yield scrapy.Request(
                url=failure.request.url, callback=self.parse, errback=self.handle_error
            )
