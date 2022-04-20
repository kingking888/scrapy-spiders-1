"""Articles spider."""
from datetime import timezone
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import CLAUDIO
from agblox.spiders.helpers import BaseSpider
import dateutil
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader


log = logging.getLogger(__name__)


class StockroverSpider(BaseSpider):
    """Spider for stockrover site."""

    name: str = "stockrover.com"
    url: str = "https://www.stockrover.com/category/blog"
    tags: List[str] = ["article", "stockrover.com"]
    host_header = "www.stockrover.com"
    spider_author = CLAUDIO

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//td/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        try:
            # There appears to be no pagination...
            next_page = etree.xpath('//a[@class="next page-numbers"]/@href')[0]
            # Is there a better way?
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        url = response.url
        # find and take out ?
        try:
            url = url.split("?", 1)[0]
        except IndexError:
            pass
        log.info(f"Article URL: {url}")

        loader = ItemLoader(item=ArticleItem(), response=response)

        # //div/a[@class='author url fn']/text()
        loader.add_value("author", self.name)

        date = response.xpath(
            '//*[@id="main-content"]/div/section/div/div[2]/section/div[1]/div/div[1]/span[1]/em//text()'
        ).get()
        iso_date = dateutil.parser.parse(date).replace(tzinfo=timezone.utc)
        loader.add_value("created_at", str(iso_date))

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='content__copy']/p//text()")
        loader.add_xpath("title", "/html/head/title//text()")
        loader.add_value("url", url)

        yield loader.load_item()
