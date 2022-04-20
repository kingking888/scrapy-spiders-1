"""MarketScreener spider."""
import logging
from typing import Iterator

from agblox.items import EquityArticleItem
from agblox.settings import EZEQUIEL
from agblox.spiders.helpers import EquitySpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class MarketScreenSpider(EquitySpider):
    """Spider for marketscreener.com site."""

    host_header = "www.marketscreener.com"
    spider_author = EZEQUIEL
    name = "marketscreener"
    tags: list = ["equity", "marketscreener", "article"]
    # urls to each ticker can't be easily created with just a ticker name, so this is currently the solution
    url_dict = {
        "twtr": "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news-history/",
        "ciic": "https://www.marketscreener.com/quote/stock/CIIG-MERGER-CORP-102588369/news-history/",
        "nga": "https://www.marketscreener.com/quote/stock/NORTHERN-GENESIS-ACQUISIT-113477460/news-history/",
        "pic": "https://www.marketscreener.com/quote/stock/PIVOTAL-INVESTMENT-CORPOR-65220663/news-history/",
        "qs": "https://www.marketscreener.com/quote/stock/QUANTUMSCAPE-CORPORATION-110986220/news-history/",
        "rmg": "https://www.marketscreener.com/quote/stock/RMG-ACQUISITION-CORP-56593825/news-history/",
        "tlry": "https://www.marketscreener.com/quote/stock/TILRAY-INC-44995241/news-history/",
        "trne": "https://www.marketscreener.com/quote/stock/TRINE-ACQUISITION-CORP-57948431/news-history/",
        "wtrh": "https://www.marketscreener.com/quote/stock/WAITR-HOLDINGS-INC-65219287/news-history/",
    }

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        for ticker, value in self.cfg["meta"]["tickers"].items():
            last_url = value.get("url")
            yield scrapy.Request(
                url=self.url_dict[ticker],
                callback=self.parse,
                cb_kwargs={"ticker": ticker, "last_url": last_url},
            )

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        articles = etree.xpath("//td[@class='newsColCT ptop3 pbottom3 pleft5 nowrap']/a/@href")
        for article in articles:
            if article == kwargs["last_url"]:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article, cb_kwargs=kwargs)
        try:
            next_page = etree.xpath("//a[@class='nPageEndTab']/@href")[0]
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse, cb_kwargs=kwargs)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=EquityArticleItem(), response=response)
        loader.add_value("author", self.name)
        loader.add_value("raw", response.text)
        tags = self.tags + [kwargs["ticker"].upper()]
        loader.add_value("tags", tags)

        loader.add_xpath("created_at", "//meta[@itemprop='datePublished']/@content")

        loader.add_xpath(
            "text",
            "//span[@itemprop='articleBody']//text()",
        )

        loader.add_xpath("title", "//h1[@itemprop='headline name']/text() ")
        loader.add_value("meta", {"base_ticker": kwargs["ticker"]})
        loader.add_value("url", response.url)
        yield loader.load_item()
