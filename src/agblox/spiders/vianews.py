"""Articles spider."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import CLAUDIO
from agblox.spiders.helpers import BaseSpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class VianewsSpider(BaseSpider):
    """Spider for via.news site."""

    host_header: str = "via.news"
    name: str = "via.news"
    tags: List[str] = ["article", "via.news"]
    spider_author = CLAUDIO

    @staticmethod
    def create_url(ticker: str) -> str:
        """Override to return equity specific url."""
        base_url_prefix = "https://via.news/?s="
        return f"{base_url_prefix}{ticker}"

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        scraped_tickers = self.cfg["meta"]["tickers"]
        for ticker in scraped_tickers:

            url = self.create_url(ticker)

            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath('//div[@class="item-details"]/h3/a/@href'):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = etree.xpath('//div[@class="page-nav td-pb-padding-side"]/a[4]/@href')[0]
            yield scrapy.Request(url=next_page, callback=self.parse)
        except IndexError:
            pass

    def parse_article(self, response: TextResponse) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)
        loader.add_xpath("created_at", "//time/@datetime")
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='td-post-content']/p//text()")
        loader.add_xpath("title", "//h1/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
