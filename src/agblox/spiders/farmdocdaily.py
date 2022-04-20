"""FarmDocDaily spiders."""
import logging
import time
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import DANIEL, USER_AGENT_SELENIUM
from agblox.spiders.helpers import BaseSpider
from lxml.html import fromstring
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

log = logging.getLogger(__name__)


class FarmDocDailySpider(BaseSpider):
    """Spider for farmdocdaily.illinois.edu site."""

    article_urls: List = []
    name = "farmdocdaily"
    url = "https://farmdocdaily.illinois.edu/"
    tags = ["article", "farmdocdaily.illinois.edu"]
    host_header = "farmdocdaily.illinois.edu"
    custom_settings = {"DOWNLOADER_MIDDLEWARES": {"scrapy_selenium.SeleniumMiddleware": 800}}
    user_agent: str = USER_AGENT_SELENIUM
    spider_author = DANIEL

    def start_requests(self) -> Iterator[SeleniumRequest]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        self.get_last_url()

        yield SeleniumRequest(url=self.url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs) -> Iterator[SeleniumRequest]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        driver: WebDriver = response.request.meta["driver"]
        driver.implicitly_wait(10)

        while True:
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[@title="Load more"]'))
                )
            except TimeoutException:
                log.warning("Button doesn't enabled")
                break

            xpath_function = """ function getElementByXpath(path) {
                              return document.evaluate(path, document, null,
                              XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            }"""

            driver.execute_script(
                xpath_function + " getElementByXpath" "('//a[@title=\"Load more\"]').click()"
            )
            time.sleep(2)

            try:
                if not driver.find_element_by_xpath('//a[@title="Load more"]').is_enabled():
                    break
            except StaleElementReferenceException:
                break

        etree = fromstring(driver.page_source)
        etree.make_links_absolute(driver.current_url)

        for article in etree.xpath('//a[@class="vc_gitem-link"]/@href'):
            if article == self.last_url:
                log.debug("Limit reached.")
                return
            yield SeleniumRequest(url=article, callback=self.parse_article)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MMMM D, YYYY")

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", '//span[@class="meta-date"]/span/text()')

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", '//div[@itemprop="text"]//text()')

        loader.add_xpath(
            "title",
            '//h1[@class="single-post-title entry-title" ' 'and @itemprop="headline"]/text()',
        )

        loader.add_value("url", response.url)

        yield loader.load_item()
