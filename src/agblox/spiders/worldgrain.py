"""World-Grain spider."""
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


class WorldGrainSpider(BaseSpider):
    """Spider for world-grain.com site."""

    name: str = "world-grain.com"
    url: str = "https://www.world-grain.com/articles/topic/1024"
    tags: List[str] = ["wheat", "article", "world-grain.com"]
    host_header = "www.world-grain.com"
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        for article in etree.xpath("//h2[@class='headline article-summary__headline']/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        next_page = etree.xpath("//a[@class='next_page']/@href")
        if not next_page:
            return
        else:
            yield scrapy.Request(next_page[0], callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MM.DD.YYYY")

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", "//div[@class='date article-summary__post-date']/text()")

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//div[@class='body gsd-paywall article-body']//text()")

        loader.add_xpath("title", "//h1[@class='page-articles-show__headline']/text()")

        loader.add_value("url", response.url)

        yield loader.load_item()
