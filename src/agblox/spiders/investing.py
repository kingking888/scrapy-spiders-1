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


class InvestingSpider(BaseSpider):
    """Spider for investing.com site."""

    name: str = "investing.com"
    url: str = "https://www.investing.com/news/forex-news"
    tags: List[str] = ["article", "investing.com", "forex"]
    host_header = "www.investing.com"
    spider_author = EZEQUIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//div[@class='textDiv']/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            if "investing.com" in article:
                yield scrapy.Request(article, callback=self.parse_article)
        next_page = etree.xpath(
            "//div[@class='sideDiv inlineblock text_align_lang_base_2']/a/@href"
        )
        if next_page:
            yield scrapy.Request(next_page[0], callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MMM DD, YYYY")
        loader.add_value("author", self.name)
        loader.add_xpath("created_at", "//div[@class='contentSectionDetails']/span/text()")
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath(
            "text", "//div[@class='WYSIWYG articlePage']//*[normalize-space(text())]/text()"
        )
        loader.add_xpath("title", "//h1[@class='articleHeader']/text()")
        loader.add_value("url", response.url)
        yield loader.load_item()
