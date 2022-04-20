"""Articles spider."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import CLAUDIO
from agblox.spiders.helpers import BaseSpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class ArstechnicaSpider(BaseSpider):
    """Spider for arstechnica.com site."""

    name: str = "arstechnica.com"
    host_header = "arstechnica.com"
    url: str = "https://arstechnica.com/"
    tags: List[str] = ["article", "arstechnica.com"]
    spider_author = CLAUDIO

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        startswith = "https://arstechnica.com/"

        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        for article in etree.xpath(
            '//section[@class="with-xrail"]//div//a[@class="overlay"]/@href'
        ):
            if article.startswith(startswith):  # skip advertisements
                if article == self.last_url:
                    log.info("Limit reached.")
                    return
                yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = etree.xpath('//a[@class="load-more"]/@href')[0]
        except IndexError:
            try:
                next_page = etree.xpath('//a[@class="left"]/@href')[0]
            except IndexError:
                pass

        if len(next_page) > 0:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)
        # date = response.xpath('//time/@data-time').get()
        loader.add_xpath("created_at", "//time/@datetime")
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", '//section[@class="article-guts"]//p//text()')
        loader.add_xpath("title", "//h1//text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
