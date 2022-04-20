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


class IowacornSpider(BaseSpider):
    """Spider for iowacorn.org site."""

    name: str = "iowacorn.org"
    url: str = "https://www.iowacorn.org/about/news/"
    tags: List[str] = ["corn", "article", "iowacorn.org"]
    host_header = "www.iowacorn.org"
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//div[@class='cms_metadata1 cms_title']/h3/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = etree.xpath(
                "//div[@class='pagination-next-page pagination-bg']"
                "/a[contains(text(),'Next')]/@href"
            )[0]
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MMMM D, YYYY")

        loader.add_value("author", self.name)
        loader.add_xpath("created_at", "//div[@class='cms_metadata2 cms_date']/h3/text()")
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='cms_content']//p//text()")
        loader.add_xpath("title", "//div[@class='w-row content-row']//h1[@class='h1']/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
