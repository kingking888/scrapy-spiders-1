"""PR News Wire Spider."""

from datetime import timezone
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import AZKA
from agblox.spiders.helpers import BaseSpider
import dateutil
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class PrNewsWireSpider(BaseSpider):
    """Spider for prnewswire.com site."""

    name: str = "prnewswire.com"
    url: str = "https://www.prnewswire.com/news-releases/news-releases-list"
    tags: List[str] = ["article", "prnewswire.com"]
    host_header = "www.prnewswire.com"
    spider_author = AZKA

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse Navigation page."""
        for link in response.xpath("//div[@class='card']/a/@href"):
            if link == self.last_url:
                log.info("Limit reached.")
                return
            yield response.follow(link.get(), callback=self.parse_article)

        next_page = response.xpath("//a[@aria-label='Next']/@href").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(response.url)
        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)
        date = response.xpath("//p[@class = 'mb-no']/text()").get()
        iso_date = dateutil.parser.parse(date).replace(tzinfo=timezone.utc)
        loader.add_value("created_at", str(iso_date))
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class = 'col-sm-10 col-sm-offset-1']//p/text()")
        loader.add_xpath("title", "//title/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
