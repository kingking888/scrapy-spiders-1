"""Cnn collection spiders."""
import logging
from typing import Iterator

from agblox.items import EquityArticleItem
from agblox.settings import ROSS
from agblox.spiders.helpers import EquitySpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class CNNSpider(EquitySpider):
    """Spider for cnn.com site."""

    host_header = "www.cnn.com"
    spider_author = ROSS
    name = "money.cnn.com"
    tags: list = ["equity", "cnn", "article"]

    @staticmethod
    def create_url(ticker: str) -> str:
        """Override to return equity specific url."""
        return f"https://money.cnn.com/quote/news/news.html?symb={ticker}"

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        scraped_tickers = ["AMZN", "TWTR"]
        for item in scraped_tickers:
            # try:
            #     last_url = scraped_tickers[item].get("url")
            # except KeyError:
            #     last_url = None
            # url = self.create_url(item)
            yield scrapy.Request(
                url=self.create_url(item),
                callback=self.parse,
                cb_kwargs={"ticker": item, "last_url": None},
            )

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        articles = etree.xpath("//h3[@class='cnn-search__result-headline']/a/@href")
        if not articles:
            log.info("No articles. Finished.")
            return
        for article in articles:
            if article == kwargs["last_url"]:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article, cb_kwargs=kwargs)
        try:
            next_page = etree.xpath(
                "//div[@class='pagination-arrow pagination-arrow-right cnnSearchPageLink text-active']"
            )[0]
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse, cb_kwargs=kwargs)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        if not response.url.startswith("https://www.cnn.com/business/live-news/"):
            return
        loader = ItemLoader(
            item=EquityArticleItem(), response=response, date_format="MMMM DD, YYYY"
        )
        loader.add_value("author", self.name)
        loader.add_value("raw", response.text)
        tags = self.tags + [kwargs["ticker"].upper()]
        loader.add_value("tags", tags)

        loader.add_xpath("created_at", "//div[@class='sc-dnqmqq hJIoKL']/text()").getall()

        loader.add_xpath("text", "//article[@class='sc-bwzfXH sc-kIPQKe jjVnED']").getall()

        loader.add_xpath("title", "//h1[@class='sc-jTzLTM sc-kkGfuU cpnQXM']/text()").get()

        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})
        loader.add_value("url", response.url)
        yield loader.load_item()
