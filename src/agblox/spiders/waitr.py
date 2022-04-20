"""WAITR press release spider."""
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


class WaitrInvestorsSpider(BaseSpider):
    """Spider for investors.waitr.com official site."""

    name: str = "investors.waitr.com"
    url: str = (
        "http://investors.waitrapp.com/news-events/news-releases?a9d908dd_year%5B"
        "value%5D=_none&page=0"
    )
    tags: List[str] = ["LeoNet", "article", "investors.waitr.com"]
    host_header = "investors.waitrapp.com"
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath(
            "//div[@class='nir-widget--field nir-widget--news--headline']/a/@href"
        ):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)

        next_page = etree.xpath("//li[@class='pager__item pager__item--next']/a/@href")

        if not next_page:
            return
        else:
            yield scrapy.Request(next_page[0], callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MMMM D, YYYY")

        loader.add_value("author", self.name)

        loader.add_xpath(
            "created_at",
            "//div[@class='field field--name-field-nir-news-"
            "date field--type-datetimezone field--label-hidden "
            "ndq-date']/div/text()",
        )

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//div[@class='node__content']//child::*/text()")

        loader.add_xpath(
            "title",
            "//div[@class='field field--name-field-nir-news-title field--"
            "type-string field--label-hidden']/div/text()",
        )

        loader.add_value("url", response.url)

        yield loader.load_item()
