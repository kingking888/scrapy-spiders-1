"""Articles spider."""

import logging
from typing import Iterator, List

from agblox.items import EquityArticleItem
from agblox.settings import YURI
from agblox.spiders.helpers import EquitySpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class NasdaqSpider(EquitySpider):
    """Spider for nasdaq.com site."""

    # because Nasdaq disallows all automated uses of their service, I am adding this download delay
    # download_delay: int = 10
    name: str = "nasdaq"
    offset: int = 1
    default_limit: int = 100  # max limit per query
    host_header: str = "www.nasdaq.com"
    tags: List[str] = ["equity", "article", "nasdaq.com"]
    spider_author = YURI

    @staticmethod
    def create_url(ticker: str, offset: int, limit: int) -> str:
        """Override to return equity specific url."""
        start = "https://www.nasdaq.com/search?q="
        page = "&page="
        url = start + ticker + page + str(offset)
        print(f"{url}\n")
        return f"{url}"

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        scraped_tickers = self.cfg["meta"]["tickers"]
        for item in scraped_tickers:
            try:
                last_url = scraped_tickers[item].get("url")
            except KeyError:
                last_url = None
            url = self.create_url(item, 1, self.default_limit)

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
        articles = etree.xpath(
            "//article[@class='search-result search-result--article']/div/div//a/@href"
        )
        print(f"\n{response.url} ... Articles found={len(articles)}\n\n")
        for article in articles:
            if article == kwargs["last_url"]:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article, cb_kwargs=kwargs)

        if articles:
            self.offset += 1
            if self.offset < self.default_limit:
                next_page = self.create_url(kwargs["ticker"], self.offset, self.default_limit)
                yield scrapy.Request(url=next_page, callback=self.parse, cb_kwargs=kwargs)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=EquityArticleItem(), response=response)

        loader.add_value("author", self.name)
        loader.add_xpath("created_at", "//div[@class='timestamp']/time/@datetime")
        loader.add_value("raw", response.text)
        tags = self.tags + [kwargs["ticker"].upper()]
        loader.add_value("tags", tags)
        loader.add_xpath("text", "//div[@class='body__content']/p//text()")
        loader.add_xpath("title", "//h1[@class='article-header__headline']/span/text()")
        loader.add_value("url", response.url)
        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})

        yield loader.load_item()
