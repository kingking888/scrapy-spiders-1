"""CNBC Equity articles spider."""
import logging
import time
from typing import Iterator

from agblox.items import EquityArticleItem
from agblox.settings import DANIEL
from agblox.spiders.helpers import EquitySpider
from itemloaders.processors import TakeFirst
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

log = logging.getLogger(__name__)


class BaseCNBCSpider(EquitySpider):
    """Base spider for cnbc.com site."""

    host_header: str = "www.cnbc.com"
    custom_settings = {"DOWNLOADER_MIDDLEWARES": {"scrapy_selenium.SeleniumMiddleware": 800}}
    spider_author = DANIEL
    name = "cnbc"

    @staticmethod
    def create_url(ticker: str) -> str:
        """Override to return equity specific url."""
        return f"https://www.cnbc.com/search/?query={ticker.upper()}"

    def start_requests(self) -> Iterator[SeleniumRequest]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        scraped_tickers = self.cfg["meta"]["tickers"]
        for ticker in scraped_tickers:
            try:
                last_url = scraped_tickers[ticker].get("url")
            except KeyError:
                last_url = None
            tags = ["article", "cnbc.com", "equity"]
            name = f"cnbc-{ticker.lower()}"
            url = self.create_url(ticker.upper())

            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                cb_kwargs={
                    "ticker": ticker,
                    "last_url": last_url,
                    "url": url,
                    "name": name,
                    "tags": tags,
                },
            )

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        driver: WebDriver = response.request.meta["driver"]
        driver.implicitly_wait(10)

        etree = fromstring(driver.page_source)
        etree.make_links_absolute(response.url)

        articles = etree.xpath("//a[@class='resultlink']")

        # to simulate keyboard presses, need to find an element in page, so body is used
        body = driver.find_element_by_css_selector("body")
        body.send_keys(Keys.PAGE_DOWN)

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

            etree = fromstring(driver.page_source)
            etree.make_links_absolute(response.url)

            new_articles = etree.xpath("//a[@class='resultlink']//@href")

            if len(new_articles) == len(articles):
                articles = new_articles
                break
            else:
                articles = new_articles

        for article in set(articles):
            if article == self.last_url:
                log.info("Limit reached.")
                return

            if "video" not in article:
                yield scrapy.Request(url=article, callback=self.parse_article, cb_kwargs=kwargs)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=EquityArticleItem(), response=response)

        loader.add_value("author", kwargs["name"])
        loader.add_value("raw", response.text)
        loader.add_value("tags", kwargs["tags"])
        loader.add_value("url", response.url)
        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})

        loader.add_xpath("created_at", "//meta[@itemprop='dateModified']/@content")
        loader.add_xpath("created_at", "//meta[@itemprop='article:modified_time']/@content")

        loader.add_xpath("text", "//div[@class='ArticleBody-articleBody']//text()")
        loader.add_xpath("text", "//div[@id='article_deck']//text()")
        loader.add_xpath("text", "//div[@id='article_body']//text()")
        loader.add_xpath("title", "//h1[@class='ArticleHeader-headline']/text()", TakeFirst())
        loader.add_xpath("title", "//h1[@class='title']/text()", TakeFirst())

        yield loader.load_item()
