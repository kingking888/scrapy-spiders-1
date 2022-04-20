"""Soy collection spiders."""
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


class TradingchartsSpider(BaseSpider):
    """Spider for trading charts soy site."""

    host_header = "futures.tradingcharts.com"
    spider_author = DANIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//div[@class='news_headlines']//li/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        # everything is in 1 page

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        loader = ItemLoader(
            item=ArticleItem(),
            response=response,
            date_format=["YYYY-MM-DD", "MMMM D, YYYY", "MMM D, YYYY", "D MMM YYYY", "MMM. D, YYYY"],
        )

        loader.add_value("author", self.name)

        created_at_str = etree.xpath("//div[@class='news_story m-cellblock m-padding']//i/text()")[
            0
        ]

        try:
            created_at_str += etree.xpath(
                "//div[@class='news_story m-cellblock m-padding']//p[2]//text()"
            )[0]
        except IndexError:
            pass

        loader.add_value("created_at", created_at_str)

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath(
            "text",
            "//div[@class='news_story m-cellblock m-padding']/pre//text() |"
            "//div[@class='news_story m-cellblock m-padding']/p//text()",
        )
        loader.add_xpath("title", "//div[@class='main_info']//h2/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
