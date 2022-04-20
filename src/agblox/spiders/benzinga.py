"""Articles spider."""
import logging
from typing import AnyStr, Dict, Iterator

from agblox.items import EquityArticleItem
from agblox.settings import ARKADY
from agblox.spiders.helpers import EquitySpider
from itemloaders.processors import TakeFirst
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class BenzingaSpider(EquitySpider):
    """Base spider for benzinga.com site."""

    host_header: str = "www.benzinga.com"
    page: int = 0
    spider_author = ARKADY
    name = "benzinga.com"

    @staticmethod
    def create_url(ticker: str) -> str:
        """Override to return equity specific url."""
        return f"https://www.benzinga.com/stock-articles/{ticker}/all"

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        scraped_tickers = self.cfg["meta"]["tickers"]
        for item in scraped_tickers:
            try:
                last_url = scraped_tickers[item].get("url")
            except KeyError:
                last_url = None
            url = self.create_url(item)
            self.url = url
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                cb_kwargs={"ticker": item, "last_url": last_url},
            )

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        articles = etree.xpath("//span[@class='field-content']/a/@href")
        if not articles:
            return

        for article in articles:
            if article == kwargs["last_url"]:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article, cb_kwargs=kwargs)

        self.page += 1
        url_query = f"?page={self.page}"

        url = f"{self.url}{url_query}"
        yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=kwargs)

    def check_field_xpath(self, response: TextResponse, field: str) -> AnyStr:
        """Helper method for check different XPaths defined in possible_paths variable."""
        possible_paths: Dict = {
            "created_at": [
                "//span[@class='date']/text()",
                "//div[@class='bz3-article-page__info']/span/text()",
            ],
            "text": [
                "//div[@class='content clear-block']//text()[normalize-space()]",
                "//div[@class='bz3-article-page__content']//text()[normalize-space()]",
            ],
            "title": ["//h1[@id='title']/text()", "//h1[@class='bz3-article-page__title']/text()"],
        }
        return next(
            (x for x in possible_paths[field] if response.selector.xpath(x).get() is not None),
            possible_paths[field][0],
        )  # match paths and return first which was found in response

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=EquityArticleItem(), response=response, date_format="MMMM D, YYYY")

        loader.add_value("author", self.name)
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags + [kwargs["ticker"].upper()])
        loader.add_value("url", response.url)
        loader.add_xpath("created_at", self.check_field_xpath(response, "created_at"), TakeFirst())
        loader.add_xpath("text", self.check_field_xpath(response, "text"))
        loader.add_xpath("title", self.check_field_xpath(response, "title"), TakeFirst())
        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})

        yield loader.load_item()
