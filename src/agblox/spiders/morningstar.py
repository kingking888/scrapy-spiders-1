"""Morning Star News Spider."""

from datetime import timezone
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import ROSS
from agblox.spiders.helpers import BaseSpider
import dateutil
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

log = logging.getLogger(__name__)


class MorningStarSpider(BaseSpider):
    """Spider for morningstar.com site."""

    name: str = "morningstar.com"
    url: str = "https://newsroom.morningstar.com/newsroom/news-archive/default.aspx"
    tags: List[str] = ["article", "morningstar.com"]
    host_header = "newsroom.morningstar.com"
    custom_settings = {"DOWNLOADER_MIDDLEWARES": {"scrapy_selenium.SeleniumMiddleware": 800}}
    spider_author = ROSS

    def start_requests(self) -> Iterator[SeleniumRequest]:
        """This method is called by Scrapy when the spider is opened for scraping.

        Args:
            None

        Yields:
            SeleniumRequest: should use it here because of dynamicaly generated page
        """
        yield SeleniumRequest(
            url=self.url,
            callback=self.parse,
        )

    def parse(self, response: HtmlResponse, **kwargs) -> Request:
        """Parse Navigation page.

        Args:
            response (HtmlResponse): an initial response from the start_request method
            kwargs (dict): can hold additional kw parameters

        Yields:
            Request: Scrapy Request for downloading a given URL
        """
        driver: WebDriver = response.request.meta["driver"]
        driver.implicitly_wait(5)

        while True:
            span_select = driver.find_element_by_xpath(
                "//div[@class='news-arch-years']//span[@class='select2-selection__arrow']"
            )
            span_select.click()

            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ModuleItemRow"))
                )
                if element:
                    links = driver.find_elements_by_xpath("//a[@class='ModuleHeadlineLink']")
                    for link in links:
                        yield self.schedule_download(link)

                remained_options = driver.find_elements_by_xpath(
                    "//li[@aria-selected='true']/following-sibling::li"
                )
                if remained_options:
                    next_opt = remained_options.pop(0)
                    next_opt_id = next_opt.get_attribute("id")
                    log.info(f"Year value: {next_opt.text}")
                    next_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, next_opt_id))
                    )
                    driver.execute_script(f"window.scrollTo(0, {next_element.size['height']});")
                    next_element.click()
                else:
                    break
            except TimeoutException:
                pass

    def schedule_download(self, link: str) -> Request:
        """Initiates Scrapy Request for given link.

        Args:
            link (str): a link path

        Returns:
            Request: a standard Scrapy Request for further yield
        """
        abs_link = link.get_attribute("href")
        log.info(f"Scheduled link: {abs_link}")
        if abs_link == self.last_url:
            log.info("Limit reached.")
            return
        return Request(url=abs_link, callback=self.parse_article)

    def parse_article(self, response: HtmlResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page.

        Args:
            response (HtmlResponse): a downloaded by Scrapy response
            kwargs (dict): additional kw data

        Returns:
            Iterator[ArticleItem]: scraped article item inside of iterator
        """
        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class = 'ModuleContentContainer']//p/text()")
        loader.add_xpath("title", "//h3[@class = 'ModuleTitle ModuleDetailHeadline']/span/text()")
        #  Parse date parameter manually because it is as text inside a tag
        date = response.xpath("//div[@class = 'ModuleDateContainer']/span/text()").get()
        parsed_date = dateutil.parser.parse(date).replace(tzinfo=timezone.utc)
        loader.add_value("created_at", str(parsed_date))
        loader.add_value("url", response.url)

        yield loader.load_item()
