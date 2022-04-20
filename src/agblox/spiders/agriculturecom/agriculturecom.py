"""Corn collection spiders."""
import logging
from typing import Iterator

from agblox.items import ArticleItem
from agblox.settings import DANIEL
from agblox.spiders.helpers import BaseSpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class AgriculturecomSpider(BaseSpider):
    """Spider for agriculture.com site."""

    host_header = "www.agriculture.com"
    first_page = True
    download_delay = 10
    spider_author = DANIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        articles = etree.xpath(
            "//div[contains(@class, 'recent-content-title-teaser')]//span[@class='field-content']/a/@href"
        )

        if not self.first_page:
            articles = articles[3:]
        else:
            self.first_page = False

        for article in articles:
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = etree.xpath(
                "//li[@class='pager__item']/a[contains(text(),'Show More')]/@href"
            )[0]
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        loader = ItemLoader(item=ArticleItem(), response=response, date_format="M/D/YYYY")

        loader.add_value("author", self.name)
        loader.add_xpath("created_at", "//div[@class='byline-date']/text()")

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//div[@class='field-body']//text()")
        loader.add_xpath("title", "//div[contains(@class,'page-primary-content')]//h1/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
