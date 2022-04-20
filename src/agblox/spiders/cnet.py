"""Articles spider."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import AZKA
from agblox.spiders.helpers import BaseSpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class CnetSpider(BaseSpider):
    """Spider for cnet.com site."""

    name: str = "cnet.com"
    host_header = "www.cnet.com"
    url: str = "https://www.cnet.com/news/"
    tags: List[str] = ["article", "cnet.com"]
    spider_author = AZKA
    download_delay = 0.2
    custom_settings = {
        "CONCURRENT_ITEMS": 10000,
        "CONCURRENT_REQUESTS": 30,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 30,
        "DOWNLOADER_MIDDLEWARES": {
            "agblox.middlewares.RotatingProxyDownloaderMiddleware": 800,
            "rotating_proxies.middlewares.BanDetectionMiddleware": 820,
            "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 830,
        },
    }

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        startswith = "https://www.cnet.com/news/"

        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        # print(f"THISURL: {response.url}\n\n")
        for article in etree.xpath('//div[contains(@class, "assetThumb")]//a/@href'):
            if article.startswith(startswith):  # skip advertisements
                if article == self.last_url:
                    log.info("Limit reached: ")
                    return

                yield scrapy.Request(article, callback=self.parse_article)
        try:
            this_url = response.url
            # Get rid of last dash
            this_url = this_url[0:-1]
            # Now check if the last word is a number
            last_character = this_url[-1]
            # If the last word is a number we must iterate past it
            if last_character.isnumeric():
                last_dash = this_url.rindex("/")
                last_dash = last_dash + 1
                this_page_number = this_url[last_dash : len(this_url)]
                if len(this_page_number) > 0:
                    pnum = int(this_page_number) + 1
                    next_page = startswith + str(pnum)
            else:
                next_page = startswith + "2"

        except IndexError:
            pass
        yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response)

        # //div/a[@class='author url fn']/text()
        loader.add_value("author", self.name)

        loader.add_xpath("created_at", "//time/@datetime")

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//article//p//text()")
        loader.add_xpath("title", "/html/head/title//text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
