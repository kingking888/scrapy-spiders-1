"""FXStreet spiders."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import ARKADY, USER_AGENT_SELENIUM
from agblox.spiders.helpers import BaseSpider
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

log = logging.getLogger(__name__)


class FXStreetSpider(BaseSpider):
    """Spider for fxstreet.com site."""

    article_urls: List = []
    name = "fxstreet.com"
    url = "https://www.fxstreet.com/news?q=&hPP=17&idx=FxsIndexPro&p=0"
    tags = ["article", "fxstreet.com"]
    host_header = "www.fxstreet.com"
    custom_settings = {"DOWNLOADER_MIDDLEWARES": {"scrapy_selenium.SeleniumMiddleware": 800}}
    user_agent: str = USER_AGENT_SELENIUM
    spider_author = ARKADY

    def start_requests(self) -> Iterator[SeleniumRequest]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        self.get_last_url()

        yield SeleniumRequest(url=self.url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        driver: WebDriver = response.request.meta["driver"]
        driver.implicitly_wait(10)

        for article in driver.find_elements_by_xpath(
            "//main[@id='hits']//div[@class='fxs_squareImage']/a"
        ):
            url = article.get_attribute("href")
            if url == self.last_url:
                log.debug("Limit reached.")
                return
            yield scrapy.Request(url=url, callback=self.parse_article)

        try:
            next_page = driver.find_element_by_xpath(
                "//section[@id='pagination_bottom']"
                "//li[@class='ais-pagination--item ais-pagination--item__next']/a"
            )
        except WebDriverException:
            pass
        else:
            url = next_page.get_attribute("href")
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)
        loader.add_xpath("created_at", "//span[@class='fxs_entry_metaInfo']/time/@datetime")
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@id='fxs_article_content']//text()")
        loader.add_xpath("title", "//article/header/h1/text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
