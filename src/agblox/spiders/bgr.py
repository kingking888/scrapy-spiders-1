"""Articles spider."""
from datetime import timezone
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import AZKA
from agblox.spiders.helpers import BaseSpider
import dateutil
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader


log = logging.getLogger(__name__)


class BgrSpider(BaseSpider):
    """Spider for bgr.com site."""

    name: str = "bgr.com"
    url: str = "https://bgr.com/tech/"
    tags: List[str] = ["article", "bgr.com"]
    spider_author = AZKA

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//article/a/@href"):

            if article.startswith("https://bgr.com"):  # skip advertisements
                if article == self.last_url:
                    log.info("Limit reached.")
                    return
                yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = etree.xpath('//a[@class="next page-numbers"]/@href')[0]
            # Is there a better way?
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response)

        # //div/a[@class='author url fn']/text()
        loader.add_value("author", self.name)

        date = response.xpath('//div[@class="text-xs text-gray-400 mt-1 lg:mt-0"]/text()').get()
        iso_date = dateutil.parser.parse(date).replace(tzinfo=timezone.utc)

        loader.add_value("created_at", str(iso_date))

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath(
            "text", '//div[@class="entry-content lg:ml-auto lg:max-w-3xl no-dropcap"]/p//text()'
        )
        loader.add_xpath("title", "/html/head/title//text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
