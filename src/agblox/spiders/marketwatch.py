"""MarketWatch Articles spider."""
from datetime import timezone
import logging
from typing import Iterator

from agblox.items import ArticleItem
from agblox.settings import DANIYAL
from agblox.spiders.helpers import EquitySpider
import dateutil
from dateutil.tz import gettz
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class MarketWatchSpider(EquitySpider):
    """Spider for MarketWatch articles."""

    host_header = "www.marketwatch.com"
    spider_author = DANIYAL
    name: str = "marketwatch"
    tags: list = ["marketwatch", "article", "equity"]
    handle_httpstatus_list = [404]

    @staticmethod
    def create_url(ticker: str) -> str:
        """Override to return equity specific url."""
        base_url_prefix = "https://www.marketwatch.com/investing/stock/"
        base_url_suffix = "/moreheadlines?channel=MarketWatch&pageNumber="
        log.info(f"Tix: {ticker}")
        return f"{base_url_prefix}{ticker}{base_url_suffix}"

    def create_funds_url(self, ticker: str) -> str:
        """Alternative url format."""
        # if it still receives 404, ticker more than likely is not given by site.
        base_url_prefix = "https://www.marketwatch.com/investing/fund/"
        base_url_suffix = "/moreheadlines?channel=MarketWatch&pageNumber="
        return f"{base_url_prefix}{ticker}{base_url_suffix}"

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
                cb_kwargs={
                    "ticker": item,
                    "last_url": last_url,
                    "page": 0,
                },
            )

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Function used to individual article urls out of all landing pages."""
        log.info(f"Ticker: {kwargs['ticker']} page: {kwargs['page']} ... URL: {response.url}")
        if response.status == 404:
            url = self.create_funds_url(kwargs["ticker"])
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                cb_kwargs={
                    "ticker": kwargs["ticker"],
                    "last_url": kwargs["last_url"],
                    "page": kwargs["page"],
                    "fund": 1,
                },
            )

        if len(response.text) < 10 or response.text.find("Page not found") >= 0:
            log.info(f"Ticker: {kwargs['ticker']} finished")
            return
        ticker = kwargs["ticker"]

        for article_block in response.xpath("//div[@class='article__content']"):
            article = article_block.xpath(
                ".//h3[@class='article__headline']/a[@class='link']/@href"
            ).get()
            # log.info(f"A={article}\nLast={kwargs['last_url']}\n\n")
            # Some articles title don't have link so cannot scrape it's data
            if article:
                if article == kwargs["last_url"]:
                    log.info(f"Limit reached... {ticker}")
                    return
            timestamp = article_block.xpath(".//span[@data-est]/text()").get()
            kwargs.update({"timestamp": timestamp})
            if article not in ["#", None]:
                try:
                    yield scrapy.Request(article, callback=self.parse_article, cb_kwargs=kwargs)
                except TypeError as e:
                    log.error("URL Type error: %s" % e)
        kwargs["page"] += 1
        if "fund" in kwargs:
            next_page = f"{self.create_funds_url(ticker)}{kwargs['page']}"
        else:
            next_page = f"{self.create_url(ticker)}{kwargs['page']}"
        yield scrapy.Request(next_page, callback=self.parse, cb_kwargs=kwargs)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {kwargs['ticker']} ... {response.url}")
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        loader = ItemLoader(item=ArticleItem(), response=response)
        loader.add_value("author", self.name)

        date = kwargs.get("timestamp")
        tzinfos = {"ET": gettz("America/New_York")}  # Specific map for timezone
        parsed_date = dateutil.parser.parse(date, tzinfos=tzinfos).replace(tzinfo=timezone.utc)

        loader.add_value("created_at", parsed_date.isoformat())
        loader.add_value("raw", response.text)
        tags = self.tags + [kwargs["ticker"].upper()]
        loader.add_value("tags", tags)
        loader.add_xpath(
            "text",
            "//div[@class='article__body article-wrap at16-col16 barrons-article-wrap']"
            "//*[self::p or self::pre]/text()",
        )
        loader.add_xpath("title", "//h1[@class='article__headline']/text()")
        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})
        loader.add_value("url", response.url)
        yield loader.load_item()
