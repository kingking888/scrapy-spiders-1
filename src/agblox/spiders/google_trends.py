"""Google Tgends Page Spider."""

import datetime
from datetime import timezone
import logging
from typing import Iterator, List
from urllib.parse import urlparse

from agblox.items import GoogleTrendsItem
from agblox.settings import YURI
from agblox.spiders.helpers import BaseSpider
import dateutil
import feedparser
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class GoogleTrendsSpider(BaseSpider):
    """Spider for trends.google.com site."""

    name: str = "trends.google.com"
    url: str = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
    tags: List[str] = ["google trends"]
    host_header = "trends.google.com"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "agblox.middlewares.RotatingProxyDownloaderMiddleware": 800,
            "agblox.middlewares.GTRetryMiddleware": 810,
            "rotating_proxies.middlewares.BanDetectionMiddleware": 820,
            "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 830,
        }
    }
    spider_author = YURI

    def start_requests(self) -> Iterator[Request]:
        """This method is called by Scrapy when the spider is opened for scraping.

        Args:
            None

        Yields:
            Request: runs headless browser for given url
        """
        yield Request(url=self.url, callback=self.parse, meta={"handle_httpstatus_list": [301]})

    def parse(self, response: HtmlResponse, **kwargs) -> None:
        """Parse Navigation page.

        Args:
            response (HtmlResponse): an initial response from the start_request method
            kwargs (dict): can hold additional kw parameters

        Yields:
            ItemLoader: Parsed page data
        """
        d = feedparser.parse(response.text)
        items = d["items"]

        loader = ItemLoader(item=GoogleTrendsItem(), response=response)

        loader.add_value("author", self.name)
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_value("text", " ")
        #  Parse date parameter manually because it is as text inside a tag
        scraped_at = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        loader.add_value("created_at", scraped_at)
        loader.add_value("url", f"{response.url}/{scraped_at}")
        loader.add_value("title", f"Daily Google Trends Data: {scraped_at}")

        meta_data = {"google_trends_data": []}

        for item in items:
            date = item["published"]
            parsed_date = dateutil.parser.parse(date).replace(tzinfo=timezone.utc).isoformat()
            meta_data["google_trends_data"].append(
                {
                    "location": urlparse(response.url).query.split("=")[1],
                    "description": item["ht_news_item_title"],
                    "title": item["title"],
                    "popularity": item["ht_approx_traffic"],
                    "source": item["ht_news_item_source"],
                    "time": str(parsed_date),
                    "url": item["ht_news_item_url"],
                }
            )

        loader.add_value("meta", meta_data)

        yield loader.load_item()
