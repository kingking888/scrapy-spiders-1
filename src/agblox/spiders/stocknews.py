"""StockNews spider."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import DANIEL
from agblox.spiders.helpers import BaseSpider
from itemloaders.processors import TakeFirst
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class StockNewsSpider(BaseSpider):
    """Spider for stocknews.com site."""

    name: str = "stocknews.com"
    url: str = "https://stocknews.com/top-stories/"
    tags: List[str] = ["equity", "article", "stocknews.com"]
    host_header = "stocknews.com"
    skip_most_popular: bool = True
    spider_author = DANIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        links = etree.xpath("//h3[@class='bold zero-margins pad-bot pad-top']/a/@href")

        if not self.skip_most_popular:
            links = links[5:]
        else:
            self.skip_most_popular = False

        if not links:
            return

        for article in links:
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)

        next_page = etree.xpath("//a[@class='btn btn-default width-full']/@href")
        if next_page:
            yield scrapy.Request(next_page[0], callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=ArticleItem(), response=response, date_format=["MMM D, YYYY"])

        loader.add_value("author", self.name)

        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        loader.add_xpath(
            "created_at",
            "//section[@class='post-meta zero-padding pad-bottom']/p/text()",
            TakeFirst(),
        )

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//article//p//text()")

        loader.add_xpath(
            "title",
            "//meta[@property='og_title']/@content | "
            "//h1[@class='page-title no-pad-left big-margin-bottom bold']"
            "//text()",
            TakeFirst(),
        )

        loader.add_value("url", response.url)

        yield loader.load_item()
