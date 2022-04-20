"""Generic MarketBeat spider."""
import logging
from typing import Any, Iterator, List

from agblox.items import EquityArticleItem
from agblox.settings import DANIEL, USER_AGENT_SELENIUM
from agblox.spiders.helpers import EquitySpider
from itemloaders.processors import TakeFirst
from lxml.html import fromstring
from scrapy import Request
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver


log = logging.getLogger(__name__)


class MarketbeatSpider(EquitySpider):
    """Spider for marketbeat.com site."""

    user_agent: str = USER_AGENT_SELENIUM
    custom_settings: dict = {"DOWNLOADER_MIDDLEWARES": {"scrapy_selenium.SeleniumMiddleware": 800}}
    host_header: str = "www.marketbeat.com"
    spider_author = DANIEL
    name: str = "marketbeat"
    tags: List[str] = ["article", "marketbeat.com", "equity"]

    @staticmethod
    def create_url(ticker: str) -> str:
        """Override to return equity specific url."""
        return f"https://www.marketbeat.com/stocks/NYSE/{ticker}/news/"

    def start_requests(self) -> Iterator[SeleniumRequest]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        tickers = self.get_tickers_from_api(5000, "volume")
        scraped_tickers = self.cfg["meta"]["tickers"]
        for item in tickers:
            try:
                last_url = scraped_tickers[item["ticker"]].get("url")
            except KeyError:
                last_url = None
            url = self.create_url(item["ticker"])
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                cb_kwargs={"url": url, "ticker": item["ticker"], "last_url": last_url},
            )

    def parse(self, response: TextResponse, **kwargs) -> Iterator[Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        driver: WebDriver = response.request.meta["driver"]
        driver.implicitly_wait(10)

        try:
            # Do this to make sure we get all marketbeat.com news
            driver.find_element_by_xpath("//option[@value='marketbeat.com']").click()
        except NoSuchElementException:
            # Some are literally the exact same webpage but listed under NASDAQ instead of NYSE
            # The easiest way to handle this is to reparse it just with NASDAQ in the URL instead
            # of NYSE
            url = kwargs["url"].replace("NYSE", "NASDAQ")
            yield SeleniumRequest(url=url, callback=self.parse, cb_kwargs=kwargs)

        etree = fromstring(driver.page_source)
        etree.make_links_absolute(driver.current_url)

        articles = set(etree.xpath("//td//a/@href"))  # Use set to remove duplicates we'll run into

        for article in articles:

            link = str(article)

            # We end up with a lot of junk links we don't want to scrape
            if (
                "www.marketbeat.com" not in link
                or "www.marketbeat.com/stocks/" in link
                or "#btm" in link
                or "short-interest" in link
            ):
                continue

            if link == self.last_url:
                log.debug("Limit reached.")
                return

            yield Request(url=link, callback=self.parse_article, cb_kwargs=kwargs)

    def _get_author_by_xpath(self, etree: Any) -> List:
        """Method for finding author[s] of the text."""
        paths: list = [
            "//span[@class='c-blue']/following-sibling::a/text()",
            "//span[@class='c-blue']/following-sibling::text()",
        ]
        authors: list = []
        for path in paths:
            authors.extend(etree.xpath(path))
        if not authors:
            authors.append("Unknown")
        return authors

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        # Sometimes we get redirected to a market-data site which we are not equipped to scrape
        # Due to redirect, we cannot catch this error before sending out request
        if "market-data" in response.url:
            return

        etree = fromstring(response.text)
        title = etree.xpath("//h1[@id='HOneTitle']//text()")

        # Sometimes we'll run into articles that no longer exist
        if title and "Error 404" in title[0]:
            return

        loader = ItemLoader(
            item=EquityArticleItem(), response=response, date_format="dddd, MMMM D, YYYY"
        )

        loader.add_value("raw", response.text)
        tags = self.tags + [kwargs["ticker"].upper()]
        loader.add_value("tags", tags)
        loader.add_value("url", response.url)
        loader.add_value("author", self._get_author_by_xpath(etree), TakeFirst())

        loader.add_xpath(
            "created_at",
            "//div[@class='d-flex align-items-start flex-wrap']"
            "//div[@class='bg-light-gray bold font-8']/text()",
            TakeFirst(),
        )

        # There's a lot of different article types so I'm just stacking all the
        # text xpaths and one of them is bound to work
        loader.add_xpath(
            "text",
            "//div[@class='headlinearticle']/p[not(contains(text(), 'Featured Article: '))]/text()",
        )
        loader.add_xpath(
            "text",
            "//div[@class='financialterm']/p[not(contains(text(), 'Featured Article: '))]/text()",
        )
        loader.add_xpath(
            "text",
            "//div[@class='instantalert']/p[not(contains(text(), 'Featured Article: '))]/text()",
        )

        loader.add_xpath("title", "//h1[@class='PageTitleHOne']//text()")
        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})

        yield loader.load_item()
