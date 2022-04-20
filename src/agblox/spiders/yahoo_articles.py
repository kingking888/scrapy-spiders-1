"""Yahoo article spider."""

import logging
import time
from typing import Iterator

from agblox.items import EquityArticleItem
from agblox.settings import DANIEL, USER_AGENT_SELENIUM
from agblox.spiders.helpers import EquitySpider
from lxml.html import fromstring
import scrapy
from scrapy.http import HtmlResponse
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

log = logging.getLogger(__name__)


class YahooBaseSpider(EquitySpider):
    """Base class for ca.finance.yahoo.com scraper."""

    user_agent: str = USER_AGENT_SELENIUM
    custom_settings = {"DOWNLOADER_MIDDLEWARES": {"scrapy_selenium.SeleniumMiddleware": 800}}
    host_header = "ca.finance.yahoo.com"
    spider_author = DANIEL
    name = "ca.finance.yahoo.com"

    @staticmethod
    def create_url(ticker: str) -> str:
        """Override to return equity specific url."""
        return f"https://ca.finance.yahoo.com/quote/{ticker}?p={ticker}"

    def start_requests(self) -> Iterator[SeleniumRequest]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        scraped_tickers = self.cfg["meta"]["tickers"]
        for item in scraped_tickers:
            try:
                last_url = scraped_tickers[item].get("url")
            except KeyError:
                last_url = None
            url = self.create_url(item)
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                cb_kwargs={"ticker": item, "last_url": last_url},
            )

    def parse(self, response: HtmlResponse, **kwargs) -> Iterator[SeleniumRequest]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        driver: WebDriver = response.request.meta["driver"]
        driver.implicitly_wait(10)

        distance_old = 0
        distance_to_top = driver.execute_script("return document.body.scrollTop;")

        # to simulate keyboard presses, need to find an element in page, so body is used
        body = driver.find_element_by_css_selector("body")
        body.send_keys(Keys.PAGE_DOWN)
        while distance_old != distance_to_top:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            distance_old = distance_to_top
            distance_to_top = driver.execute_script("return document.body.scrollTop);")

        etree = fromstring(driver.page_source)
        etree.make_links_absolute(response.url)

        for article in etree.xpath("//h3[@class='Mb(5px)']/a/@href"):
            if article == kwargs["last_url"]:
                log.info("Limit reached.")
                return
            yield scrapy.Request(url=article, callback=self.parse_article, cb_kwargs=kwargs)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=EquityArticleItem(), response=response)
        loader.add_value("raw", response.text)
        loader.add_value("url", response.url)
        tags = self.tags + [kwargs["ticker"].upper(), self.name]
        loader.add_value("tags", tags)
        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})
        loader.add_value("author", self.name)
        loader.add_xpath("created_at", "//div[@class='caas-attr-time-style']/time/@datetime")
        loader.add_xpath("title", "//h1[@data-test-locator='headline']/text()")
        loader.add_xpath("text", "//div[@class='caas-body']//text()")

        yield loader.load_item()
