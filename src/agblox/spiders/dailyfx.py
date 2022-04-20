"""Forex collection spiders."""
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


class DailyfxSpider(BaseSpider):
    """Spider for dailyfx.com site."""

    name: str = "dailyfx"
    url: str = "https://www.dailyfx.com/market-news/articles"
    tags: List[str] = ["forex", "article", "dailyfx"]
    host_header = "www.dailyfx.com"
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath(
            "//div[@class='dfx-articleList jsdfx-articleList  ']"
            "//a[@class='dfx-articleListItem jsdfx-articleListItem d-flex mb-3']/@href"
        ):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = etree.xpath("//a[@class='dfx-paginator__link  ml-auto']/@href")[0]
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)
        loader.add_xpath(
            "created_at", "//time[@class='dfx-articleHead__displayDate d-block']/@data-time"
        )
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        text_xpath = (
            "//div[@class='dfx-articleBody__content']/h2[@class='article-subheader']/text() |"
            " //div[@class='dfx-articleBody__content']//span/text()"
        )
        loader.add_xpath("text", text_xpath)
        loader.add_xpath("title", "//h1[@class='dfx-articleHead__header m-0']/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
