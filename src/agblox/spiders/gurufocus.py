"""Article spider."""

import logging
import time
from typing import Iterator, List

from agblox.items import EquityArticleItem
from agblox.settings import DANIEL, USER_AGENT_SELENIUM
from agblox.spiders.helpers import EquitySpider
from itemloaders.processors import TakeFirst
from lxml.html import fromstring
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

log = logging.getLogger(__name__)


class GurufocusBaseSpider(EquitySpider):
    """Base class for gurufocus.com scraper."""

    user_agent: str = USER_AGENT_SELENIUM
    custom_settings = {"DOWNLOADER_MIDDLEWARES": {"scrapy_selenium.SeleniumMiddleware": 800}}
    spider_author = DANIEL
    name = "gurufocus.com"
    host_header = "www.gurufocus.com"

    @staticmethod
    def create_url(ticker: str) -> str:
        """Override to return equity specific url."""
        return f"https://www.gurufocus.com/stock/{ticker}/article"

    def start_requests(self) -> Iterator[SeleniumRequest]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        scraped_tickers = self.cfg["meta"]["tickers"]
        for item in scraped_tickers:
            try:
                last_url = scraped_tickers[item].get("url")
            except KeyError:
                last_url = None
            self.tags += [item, "article", "gurufocus.com"]
            url = self.create_url(item)

            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                cb_kwargs={
                    "ticker": item,
                    "last_url": last_url,
                    "url": url,
                    "tags": self.tags,
                },
            )

    def parse(self, response: HtmlResponse, **kwargs) -> Iterator[SeleniumRequest]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        driver: WebDriver = response.request.meta["driver"]
        driver.implicitly_wait(30)

        article_urls: List = []

        try:
            while driver.find_element_by_class_name("btn-next").is_enabled():
                try:
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "btn-next"))
                    )
                except TimeoutException:
                    log.warning("Button doesn't enabled")
                    article_urls.extend(self.extract_articles(driver.page_source, response.url))
                    break

                article_urls.extend(self.extract_articles(driver.page_source, response.url))
                if kwargs["last_url"] in article_urls:
                    log.info("Limit reached.")
                    break
                driver.execute_script("document.getElementsByClassName('btn-next')[0].click()")
                time.sleep(2)
            else:
                # if it's the last or the single page
                article_urls.extend(self.extract_articles(driver.page_source, response.url))
        except NoSuchElementException:
            log.info("Failed to find btn-next for gurufocus")

        if kwargs["last_url"] in article_urls:
            last_index = article_urls.index(kwargs["last_url"])
            article_urls = article_urls[:last_index]

        for article in set(article_urls):
            yield SeleniumRequest(url=article, callback=self.parse_article, cb_kwargs=kwargs)

    def extract_articles(self, page_source: str, url: str) -> List[str]:
        """Extract article urls from page."""
        etree = fromstring(page_source)
        etree.make_links_absolute(url)

        return etree.xpath(
            "//div[@class='el-col'][1]//div[@class='fs-large color-primary']//a/@href"
        )

    def parse_article(self, response: HtmlResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Method which save articles."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=EquityArticleItem(), response=response, date_format="MMMM D, YYYY")

        loader.add_value("raw", response.text)
        loader.add_value("tags", kwargs["tags"])
        loader.add_value("url", response.url)
        loader.add_value("author", self.name)
        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})

        loader.add_xpath("created_at", "//span[@class='date']/text()", TakeFirst())

        loader.add_xpath("title", "//h1/text()")

        loader.add_xpath("text", "//div[@id='articlebody_new']//text()")

        yield loader.load_item()
