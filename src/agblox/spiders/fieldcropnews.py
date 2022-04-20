"""fieldcropnews spiders."""
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


class FieldCropNewsSpider(BaseSpider):
    """Spider for fieldcropnews.com."""

    name: str = "fieldcropnews.com"
    url: str = "https://fieldcropnews.com/"
    tags: List[str] = ["article", "fieldcropnews.com"]
    host_header = "fieldcropnews.com"
    spider_author = DANIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//div[@class='entry-title']/h2/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)

        next_page = etree.xpath('//a[@class="next-post"]/@href')

        if not next_page:
            return
        else:
            yield scrapy.Request(next_page[0], callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MMMM D, YYYY")

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", "//span[@class='post-date']/text()", TakeFirst())

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", '//div[@class="entry-content"]//text()')

        loader.add_xpath("title", "//span[@itemprop='name headline']/text()")

        loader.add_value("url", response.url)

        yield loader.load_item()
