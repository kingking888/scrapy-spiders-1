"""Smarter Analyst spider."""
import logging
from typing import Iterator, List

from agblox.items import EquityArticleItem
from agblox.settings import EZEQUIEL
from agblox.spiders.helpers import EquitySpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

log = logging.getLogger(__name__)


class SmarterAnalystSpider(EquitySpider):
    """Spider for SmarterAnalyst.com site."""

    name: str = "smarteranalyst"
    tags: List[str] = ["article", "smarteranalyst", "equity"]
    host_header = "www.smarteranalyst.com"
    spider_author = EZEQUIEL

    @staticmethod
    def create_url(ticker: str) -> str:
        """Override to return equity specific url."""
        base_url_prefix = "https://www.smarteranalyst.com/?s="
        return f"{base_url_prefix}{ticker}"

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        scraped_tickers = self.cfg["meta"]["tickers"]
        for item in scraped_tickers:
            try:
                last_url = scraped_tickers[item].get("url")
            except KeyError:
                last_url = None
            url = self.create_url(item)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                cb_kwargs={"ticker": item, "last_url": last_url},
            )

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//h2[@class='title']/a/@href | //h3[@class='title']/a/@href"):
            if article == kwargs["last_url"]:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article, cb_kwargs=kwargs)
        try:
            next_page = etree.xpath("//a[@class='next page-numbers']/@href")[0]
        except IndexError:
            return
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, cb_kwargs=kwargs)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        loader = ItemLoader(item=EquityArticleItem(), response=response, date_format="MMMM D, YYYY")
        loader.add_value("author", self.name)
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        created_at = "".join(etree.xpath("//div[@class='post-meta header-font']/text()")).replace(
            "\n", ""
        )
        loader.add_value("created_at", created_at)
        loader.add_value("raw", response.text)
        tags = self.tags + [kwargs["ticker"].upper()]
        loader.add_value("tags", tags)
        text = "\n".join(
            response.xpath(
                "//div[@class='post-content clearfix']/p[not(contains(text(), 'Related News'))]"
            ).getall()
        )
        loader.add_value("text", remove_tags(text))
        loader.add_xpath(
            "title",
            "//h1[@class='post-title title title-large entry-title  ']/text() |"
            "//h1[@class='post-title title title-large entry-title contributor ']/text()",
        )
        loader.add_value("url", response.url)
        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})

        yield loader.load_item()
