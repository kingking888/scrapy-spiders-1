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


class CanadiancattlemanSpider(BaseSpider):
    """Spider for canadiancattleman.ca site."""

    name: str = "canadiancattleman.ca"
    url: str = "https://www.canadiancattlemen.ca/news/"
    tags: List[str] = ["slaughter cattle", "article", "canadiancattleman.ca"]
    host_header = "www.canadiancattlemen.ca"
    page = 1
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        articles = etree.xpath(
            "//div[@class='archive-articles-list']//h2[@class='entry-title']/a/@href"
        )

        if not articles:
            return

        for article in articles:
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        self.page += 1
        yield scrapy.Request(url=f"{self.url}page/{self.page}/", callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=ArticleItem(), response=response, date_format="YYYY-MM-DD")

        loader.add_value("author", self.name)
        loader.add_xpath("created_at", "//span[@content]/@content")
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='body-text']//p/text()")
        loader.add_xpath("title", "//h1[@class='entry-title']/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
