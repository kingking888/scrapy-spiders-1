"""Fool.com news spider."""
import logging
import re
import time
from typing import Iterator, List

from agblox.items import EquityArticleItem
from agblox.settings import USER_AGENT_SELENIUM, YURI
from agblox.spiders.helpers import EquitySpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

log = logging.getLogger(__name__)


class FoolSpider(EquitySpider):
    """Spider for fool.com news source."""

    article_urls: List = []
    host_header = "www.fool.com"
    spider_author = YURI
    name = "fool"
    tags: list = ["equity", "fool", "article"]

    user_agent: str = USER_AGENT_SELENIUM

    custom_settings = {"DOWNLOADER_MIDDLEWARES": {"scrapy_selenium.SeleniumMiddleware": 800}}

    equity_suffixes_mapper: dict = {
        "twtr": ("nyse", "twitter"),
        "ciic": ("nasdaq", "ciig-merger"),
        "fsr": ("nyse", "fisker"),
        "nga": ("nyse", "northern-genesis-acquisition"),
        "pic": ("nyse", "pivotal-investment-corporation-ii"),
        "qs": ("nyse", "quantumscape"),
        "rmg": ("nyse", "rmg-acquisition"),
        "tlry": ("nasdaq", "tilray-inc"),
        "trne": ("nyse", "trine-acquisition"),
        "wtrh": ("nasdaq", "waitr-holdings"),
    }

    @staticmethod
    def create_url(ticker: str, suffixes: dict) -> str:
        """Creating url for calling the fool.com for apropriate ticker."""
        base_url: str = (
            f"https://www.fool.com/quote/{suffixes[ticker][0]}/{suffixes[ticker][1]}/{ticker}/"
        )
        return base_url

    def start_requests(self) -> Iterator[SeleniumRequest]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        for ticker, val in self.cfg["meta"]["tickers"].items():
            self.last_url = val.get("url")
            url = self.create_url(ticker, self.equity_suffixes_mapper)
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                cb_kwargs={"ticker": ticker, "last_url": self.last_url},
            )

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse page with articles urls from fool.com."""
        log.info(f"Article URL: {response.url}")
        driver: WebDriver = response.request.meta["driver"]
        driver.implicitly_wait(10)
        load_btn_xpath = "//button[@id='load-more' and @data-type='all']"
        is_load_btn = self._check_element_exists(driver, load_btn_xpath)
        while is_load_btn:
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, load_btn_xpath))
                )
            except TimeoutException:
                log.warning("Button doesn't enabled.")
                break

            self.article_urls.extend(
                self.extract_articles(driver.page_source, response.url, **kwargs)
            )
            if self.last_url in self.article_urls:
                log.info("Limit reached.")
                break
            driver.find_element_by_xpath(load_btn_xpath).click()
            time.sleep(2)

            is_load_btn = self._check_element_exists(driver, load_btn_xpath)

        for url in self.article_urls:
            if url == kwargs["last_url"]:
                log.info("Limit reached.")
                return
            yield scrapy.Request(url, callback=self.parse_article, cb_kwargs=kwargs)

    def extract_articles(self, page_source: str, url: str, **kwargs) -> List[str]:
        """Extract article urls from page."""
        etree = fromstring(page_source)
        etree.make_links_absolute(url)
        articles = etree.xpath("//a[@data-id='article-list-hl']/@href")
        return articles

    def _get_pub_date(self, url: str) -> str:
        """Returns mached publicationdate from url string."""
        pub_date = re.findall(r"[\d]{1,4}/[\d]{1,2}/[\d]{1,2}", url)[0]
        return pub_date

    def _check_element_exists(self, driver: object, path: str) -> bool:
        """Checks if given element exists in page source."""
        try:
            driver.find_element_by_xpath(path)
            if_exists = True
        except NoSuchElementException as e:
            log.warning(e.msg)
            if_exists = False
        return if_exists

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=EquityArticleItem(), response=response, date_format="YYYY/MM/DD")
        loader.add_xpath("author", "//div[@class='author-name']/a/text()")
        loader.add_value("raw", response.text)
        tags = self.tags + [kwargs["ticker"].upper()]
        loader.add_value("tags", tags)
        loader.add_value("created_at", self._get_pub_date(response.url))
        loader.add_xpath("text", "//span[@class='article-content']/*[not(div[@id='pitch'])]/text()")
        loader.add_xpath("title", "//h1/text()")
        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})
        loader.add_value("url", response.url)
        yield loader.load_item()
