"""GlobeAndMail collection spiders."""
import json
from json.decoder import JSONDecodeError
import logging
import time
from typing import Iterator


from agblox.items import EquityArticleItem
from agblox.settings import AZKA
from agblox.spiders.helpers import EquitySpider
import arrow
from lxml.html import fromstring
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import JsonRequest, TextResponse
from scrapy.loader import ItemLoader
from scrapy.settings import Settings
from scrapy_selenium import SeleniumRequest

log = logging.getLogger(__name__)


class GlobeAndMailSpider(EquitySpider):
    """Spider for theglobeandmail.com site."""

    name: str = "theglobeandmail"
    spider_author: str = AZKA
    tags: list = ["equity", "globeandmail", "article"]
    base_url: str = "https://www.theglobeandmail.com"
    handle_httpstatus_list = [404, 500]

    @classmethod
    def update_settings(cls, settings: Settings) -> None:
        """Customize spider settings."""
        cls.custom_settings["DEFAULT_REQUEST_HEADERS"] = {"user-agent": cls.user_agent}
        cls.custom_settings["DOWNLOAD_DELAY"] = cls.download_delay
        settings.setdict(cls.custom_settings or {}, priority="spider")

    @staticmethod
    def create_url(ticker: str) -> str:
        """Equity specific url."""
        return "https://globeandmail.pl.barchart.com/module/News.json"

    def start_requests(self) -> Iterator[SeleniumRequest]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        scraped_tickers = self.cfg["meta"]["tickers"]
        for item in scraped_tickers:
            try:
                last_url = scraped_tickers[item].get("url")
            except KeyError:
                last_url = None
            yield JsonRequest(
                url=self.create_url(item),
                callback=self.parse,
                cb_kwargs={"ticker": item, "last_url": last_url},
                method="POST",
                data={"before": int(time.time()), "symbol": item.upper()},
            )

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        if response.status != 200:
            log.info(
                f"The url {response.url} doesn't return response. Response status code is {response.status}"
            )
            raise CloseSpider(response.body)

        try:
            body = json.loads(response.text)
        except JSONDecodeError:
            log.warning(f"Unable to get json body for: {response.url}")
            return

        if not body["stories"]:
            log.info(f"Ticker: {kwargs['ticker']} finished")
            return

        article_link = body["link"]

        for story in body["stories"]:
            url = f"{self.base_url}{article_link}"
            url = url.format(storyId=story["id"])
            if url == kwargs["last_url"]:
                log.info("Limit reached.")
                return
            yield scrapy.Request(
                url=url,
                callback=self.parse_article,
                cb_kwargs=kwargs,
            )

        yield JsonRequest(
            url=self.create_url(kwargs["ticker"]),
            callback=self.parse,
            cb_kwargs=kwargs,
            method="POST",
            data={"before": body["stories"][-1]["timestamp"], "symbol": kwargs["ticker"].upper()},
        )

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Parse article page."""
        if response.status == 404:
            log.info(f"Article not found in URL: {response.url}")
            return

        log.info(f"Article URL: {response.url}")
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        loader = ItemLoader(item=EquityArticleItem(), response=response)

        loader.add_value("raw", response.text)
        tags = self.tags + [kwargs["ticker"].upper()]
        loader.add_value("tags", tags)
        loader.add_value("url", response.url)
        loader.add_value("author", self.name)
        created_at = etree.xpath("//span[@class='published']/text()")[0]
        created_at = arrow.get(created_at, "ddd MMM D").replace(
            year=int(arrow.now().format("YYYY"))
        )
        if created_at > arrow.now():  # change year to previous year if article is old
            created_at = created_at.replace(year=int(arrow.now().format("YYYY")) - 1)
        loader.add_value("created_at", created_at.for_json())
        loader.add_xpath("text", "//div[@class='content']//text()")
        loader.add_xpath("title", "//h1[@class='story-title']/text()")
        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})

        yield loader.load_item()
