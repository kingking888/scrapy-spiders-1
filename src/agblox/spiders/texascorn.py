"""Articles spider."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import EZEQUIEL
from agblox.spiders.helpers import BaseSpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class TexasCornSpider(BaseSpider):
    """Spider for texascorn.org site."""

    name: str = "texascorn.org"
    url: str = "https://texascorn.org/page/1/?s=&id=1&post_type=post"
    tags: List[str] = ["article", "texascorn.org"]
    spider_author = EZEQUIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//div[@class='inner-wrap']/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = etree.xpath("//div[@class='next']/a/@href")[0]
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MMMM D, YYYY")

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", "//span[@class='meta-date date updated']/text()")
        loader.add_xpath("created_at", "//span[@class='meta-date date published']/text()")

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//div[@class='wpb_wrapper' or @class='pf-content']//text()")
        loader.add_xpath("title", "//div[@class='inner-wrap']//h1/text()")

        loader.add_value("url", response.url)

        yield loader.load_item()
