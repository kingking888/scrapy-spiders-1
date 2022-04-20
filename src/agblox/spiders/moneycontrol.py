"""Articles spider."""
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


class MoneycontrolSpider(BaseSpider):
    """Spider for Penn State articles."""

    name: str = "moneycontrol.com"
    url: str = "https://www.moneycontrol.com/news/tags/soybean.html/page-1/"
    tags: List[str] = ["article", "moneycontrol.com"]
    host_header = "www.moneycontrol.com"
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Function used to individual article urls out of all landing pages."""
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//li[@class='clearfix']/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        next_page = etree.xpath("//a[@class='last']/@href")
        if next_page:
            yield scrapy.Request(next_page[0], callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response)
        loader.add_value("author", self.name)

        loader.add_xpath("created_at", '//meta[@name="Last-Modified"]/@content')

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath(
            "text", "//div[@class='content_wrapper arti-flow']/p[normalize-space(text())]//text()"
        )

        loader.add_xpath("title", "//h1[@class='article_title artTitle']/text()")

        loader.add_value("url", response.url)

        yield loader.load_item()
