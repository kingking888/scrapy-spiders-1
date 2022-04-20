"""Zacks collection spiders."""
import logging
from typing import Iterator

from agblox.items import EquityArticleItem
from agblox.settings import EZEQUIEL
from agblox.spiders.helpers import EquitySpider, headers
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class ZacksSpider(EquitySpider):
    """Spider for zacks.com site."""

    host_header = "www.zacks.com"
    spider_author = EZEQUIEL
    name = "zacks"
    tags: list = ["equity", "zacks", "article"]
    headers = {"Authority": "www.zacks.com"}

    @staticmethod
    def create_url(ticker: str) -> str:
        """Override to return equity specific url."""
        base_url_prefix = "https://www.zacks.com/stock/research/"
        base_url_suffix = "/all-news/zacks"
        return f"{base_url_prefix}{ticker}{base_url_suffix}"

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        scraped_tickers = self.cfg["meta"]["tickers"]
        custom_headers = headers(self.host_header)
        for item in scraped_tickers:
            try:
                last_url = scraped_tickers[item].get("url")
            except KeyError:
                last_url = None
            url = self.create_url(item)
            h = {
                "authority": "www.zacks.com",
                "method": "GET",
                "path": f"/stock/research/{item}/all-news/zacks",
                "scheme": "https",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8,application/"
                "signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "cache-control": "max-age=0",
                "accept-language": "en-US,en;q=0.9",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) "
                "AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 "
                "Mobile/14E304 Safari/602.1",
            }
            custom_headers.update(h)
            yield scrapy.Request(
                url=url,
                headers=h,
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
        articles = etree.xpath("//h1[@class='truncated_text_single']/a/@href")
        if not articles:
            log.info("No articles. Finished.")
            return
        for article in articles:
            if article == kwargs["last_url"]:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article, cb_kwargs=kwargs)
        try:
            next_page = etree.xpath("//a[@rel='next']/@href")[0]
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse, cb_kwargs=kwargs)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        if not response.url.startswith("https://www.zacks.com/stock/news"):
            return
        loader = ItemLoader(
            item=EquityArticleItem(), response=response, date_format="MMMM DD, YYYY"
        )
        loader.add_value("author", self.name)
        loader.add_value("raw", response.text)
        tags = self.tags + [kwargs["ticker"].upper()]
        loader.add_value("tags", tags)

        loader.add_xpath(
            "created_at", "//p[@class='byline']/span/time/text() | //p[@class='byline']/time/text()"
        )

        loader.add_xpath(
            "text",
            "//div[@id='comtext']//text() | //section[@class='reserach_daily_reports']//text()",
        )

        loader.add_xpath(
            "title",
            "//section[@id='commentary_article']/article/h1/text() "
            "| //header[@class='mugshot_large']/h1/text()",
        )
        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})
        loader.add_value("url", response.url)
        yield loader.load_item()
