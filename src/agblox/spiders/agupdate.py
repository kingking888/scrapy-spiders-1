"""Articles spider."""
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


class AgupdateSpider(BaseSpider):
    """Spider for agupdate.com site."""

    name: str = "agupdate.com"
    url: str = "https://www.agupdate.com/search/?k=%22corn%22&l=10#tncms-source=keyword&l=10"
    tags: List[str] = ["article", "agupdate.com"]
    host_header = "www.agupdate.com"
    spider_author = DANIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//h3[@class='tnt-headline ']/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        next_page = etree.xpath("//li[@class='next']/a/@href")
        if next_page:
            yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)

        created_at_xpath = "//time[@class='tnt-date asset-date text-muted']/@datetime"
        loader.add_xpath("created_at", created_at_xpath, TakeFirst())

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        text_xpath = "//div[contains(@class, 'main-content')]//p//text()"

        loader.add_xpath("text", text_xpath)

        title_xpath = "//h1[@class='headline']/span/text()[normalize-space()]"
        loader.add_xpath("title", title_xpath, TakeFirst())

        loader.add_value("url", response.url)

        yield loader.load_item()
