"""Forex collection spiders."""
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


class ForexWorldSpider(BaseSpider):
    """Spider for forexnews.world site."""

    name: str = "forexnews.world"
    url: str = "https://www.forexnews.world/category/forex/page/1/"
    tags: List[str] = ["forex", "article", "forexnews.world"]
    host_header = "www.forexnews.world"
    page = 1
    base_url = "https://www.forexnews.world/category/forex/page/"
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        articles = etree.xpath("//div[@class='td-module-thumb']/a/@href")

        if not articles:
            return

        for article in articles:
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        self.page += 1
        next_page = f"{self.base_url}{self.page}"
        yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)
        loader.add_xpath(
            "created_at", "//div[@class='tdb-block-inner td-fix-index']/time/@datetime"
        )
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='tdb-block-inner td-fix-index']//text()")
        loader.add_xpath("title", "//div[@class='tdb-block-inner td-fix-index']/h1/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
