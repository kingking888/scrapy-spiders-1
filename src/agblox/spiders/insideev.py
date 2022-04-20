"""FSR collection spiders."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import DANIEL
from agblox.spiders.helpers import BaseSpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class InsideEvSpider(BaseSpider):
    """Spider for insideevs.com site."""

    name: str = "insideevs.com"
    url: str = "https://insideevs.com/fisker/karma/news/"
    tags: List[str] = ["FSR", "article", "insideevs-FSR"]
    spider_author = DANIEL

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//h3/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = etree.xpath("//a[@data-id='nextPage']/@href")[0]
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MMM DD, YYYY")

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", "//span[@class='date']/a/text()")

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//div[@class='postBody description e-content']//text()")

        loader.add_xpath("title", "//h1[@class='m1-article-title']/text()")

        loader.add_value("url", response.url)

        yield loader.load_item()
