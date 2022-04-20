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


class InvestopediaCompanyNewsSpider(BaseSpider):
    """Spider for investopediasite."""

    name: str = "investopedia-company_news"
    url: str = "https://www.investopedia.com/company-news-4427705"
    tags: List[str] = ["article", "investopedia.com"]
    host_header = "www.investopedia.com"
    spider_author = DANIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//div[@class='card__content']/parent::a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)

        # Investopedia is all one page

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MMM D, YYYY")

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", "//div[starts-with(@id, 'displayed-date')]/text()")

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//div[starts-with(@id, 'article-body')]//text()")
        loader.add_xpath("title", "//h1[starts-with(@id, 'article-heading')]/text()")

        loader.add_value("url", response.url)

        yield loader.load_item()
