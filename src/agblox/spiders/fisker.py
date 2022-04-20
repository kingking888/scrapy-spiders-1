"""Fisker corporate news spiders."""
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


class FiskerInvestorSpider(BaseSpider):
    """Spider for investors.fiskerinc.com site."""

    name: str = "investors.fiskerinc.com"
    url: str = "https://investors.fiskerinc.com/news/default.aspx"
    tags: List[str] = ["FSR", "article", "investors.fiskerinc.com"]
    host_header = "investors.fiskerinc.com"
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//div[@class='module_headline']/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        # everything is in 1 page

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MM/DD/YYYY")

        loader.add_value("author", self.name)
        loader.add_xpath("created_at", "//div[@class='module_date-time']/span/text()")
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='module_body']//p//text()")
        loader.add_xpath("title", "//h3[@class='module-details_title']/span/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
