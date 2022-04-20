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


class CropwatchSpider(BaseSpider):
    """Spider for cropwatch.unl.edu site."""

    name: str = "cropwatch.unl.edu"
    url: str = "https://cropwatch.unl.edu/tags/soybean"
    tags: List[str] = ["article", "cropwatch.unl.edu"]
    host_header = "cropwatch.unl.edu"
    spider_author = DANIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath(
            "//h3[@class='wdn-brand clear-top dcf-txt-h4 dcf-mb-0']/a/@href"
        ):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        next_page = etree.xpath("//li[@class='pager-next']/a/@href")
        if next_page:
            yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MMMM D, YYYY")

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", "//span[@class='date-display-single']/text()")

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//div[@class='field-item even']//text()")

        loader.add_xpath("title", "//div[@class='content']/div/h1/text()")

        loader.add_value("url", response.url)

        yield loader.load_item()
