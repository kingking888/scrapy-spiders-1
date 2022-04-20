"""Reddit spider."""
from datetime import datetime, timezone
import json
import logging
from typing import Any, Dict, Iterator, Optional
from urllib.parse import urlencode

from agblox.items import RedditSearchItem
from agblox.settings import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_PASSWORD,
    REDDIT_USERNAME,
    YURI,
)
from agblox.spiders.helpers import EquitySpider, SpiderConfigurationError
import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse
from scrapy.http import Response
from scrapy.loader import ItemLoader
from scrapy.settings import Settings

log = logging.getLogger(__name__)


class RedditSearchSpider(EquitySpider):
    """Spider for reddit.com site."""

    name: str = "reddit.stocks.search"
    spider_author = YURI
    custom_settings = {
        "ITEM_PIPELINES": {
            "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 300,
            "agblox.pipelines.LanguageDetectionPipeline": 305,
            "agblox.pipelines.FSPipeline": 310,
            "agblox.pipelines.S3Pipeline": 320,
            "agblox.pipelines.TopicClassificationPipeline": 330,
            "agblox.pipelines.APIPipeline": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        }
    }
    download_delay = 1
    handle_httpstatus_list = [401, 501]

    http_user = REDDIT_USERNAME
    http_pass = REDDIT_PASSWORD
    client_id = REDDIT_CLIENT_ID
    client_secret = REDDIT_CLIENT_SECRET

    headers = {"User-Agent": "DiviAIApp/0.1.0 by /u/yugritsai email: yugritsai@gmail.com"}

    def __init__(self, *args, **kwargs) -> None:
        """Hide WARNNING log level from validation."""
        logger = logging.getLogger("scrapy.core.scraper")
        logger.setLevel(logging.ERROR)
        super().__init__(*args, **kwargs)

    @classmethod
    def update_settings(cls, settings: Settings) -> None:
        """Customize spider settings."""
        cls.custom_settings["DEFAULT_REQUEST_HEADERS"] = cls.headers
        cls.custom_settings["DOWNLOAD_DELAY"] = cls.download_delay
        cls.custom_settings["DOWNLOADER_MIDDLEWARES"] = {
            "agblox.middlewares.RedditDownloaderMiddleware": 100
        }
        settings.setdict(cls.custom_settings or {}, priority="spider")

    @classmethod
    def from_crawler(cls, crawler: Any, *args, **kwargs) -> "RedditSearchSpider":
        """This method is used by Scrapy to create your spiders."""
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        cls.config = kwargs.get("config")
        cls.cfg = cls.get_cfg()
        crawler.cfg = cls.cfg
        return spider

    @classmethod
    def get_cfg(cls) -> Dict[str, Any]:
        """Read spider configuration."""
        try:
            cfg = cls.get_cfg_from_file()
        except Exception as e:
            log.info(f"Can't read configuration from file for [{cls.name}]. {e}")
        else:
            return cfg
        try:
            cfg = cls.get_spider_conf_tickers()
        except Exception as e:
            log.info(f"Can't read configuration from API. {e}")
        else:
            return cfg
        raise SpiderConfigurationError("Can't read spider configuration.")

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping.

        We use it to obtain initial TOKEN from Reddit.
        """
        self.auth_payload = {
            "grant_type": "password",
            "username": self.http_user,
            "password": self.http_pass,
        }

        yield Request(
            url="https://www.reddit.com/api/v1/access_token",
            method="POST",
            body=urlencode(self.auth_payload),
            headers=self.headers,
            callback=self.parse,
        )

    def add_item(self, item: Dict, ticker: str) -> Optional[RedditSearchItem]:
        """Method for add item to ItemLoader."""
        link = f"https://www.reddit.com{item['permalink']}"
        try:
            loader = ItemLoader(item=RedditSearchItem())
            loader.add_value("text", item["selftext"])
            loader.add_value("author", self.name)
            loader.add_value("title", item["title"])
            loader.add_value("url", link)
            loader.add_value("raw", item["selftext_html"])
            loader.add_value(
                "tags", self.tags + ["reddit", item["subreddit"], item["author"], ticker]
            )
            created_at = datetime.utcfromtimestamp(item["created_utc"]).replace(tzinfo=timezone.utc)
            loader.add_value("created_at", created_at.isoformat())

            post_data = {
                "base_ticker": ticker,
                "subreddit": item["subreddit"],
                "reddit_data": {
                    "post_author": item["author"],
                    "last_comment_id": None,
                    "submission_id": item["id"],
                },
            }

            loader.add_value("meta", post_data)
            log.info(f"Downloaded Reddit's submission: {link}. Adding...")
            return loader.load_item()
        except Exception:
            log.error(f"Was problem with: {link}", exc_info=True)
            return None

    def parse(self, response: Response, **kwargs) -> Request:
        """Used for parsing downloader responses."""
        if response.status != 200:
            raise CloseSpider(response.body)
        # self.update_token(response)
        self.tickers = self.cfg["meta"]["tickers"]
        for ticker in self.tickers:

            log.info(f"Starting search for ticker: ${ticker}")
            try:
                data = self.get_last_url_for_tag(ticker)
                last_sub = data[0].get("url")
            except (KeyError, IndexError):
                last_sub = None

            payload: dict = {"q": f"${ticker}", "limit": 1000, "sort": "new", "t": "all"}

            yield Request(
                url=f"https://oauth.reddit.com/search.json?{urlencode(payload)}",
                headers=self.headers,
                callback=self.parse_search_result,
                cb_kwargs={"last_sub": last_sub, "ticker": ticker},
            )

    def parse_search_result(self, response: HtmlResponse, **kwargs) -> None:
        """Parse each returned listing from Reddit."""
        if response.status != 200:
            raise CloseSpider(response.json())
        r = json.loads(response.body)
        after = r["data"]["after"]
        items = r["data"]["children"]
        limited = False
        for item in items:
            # log.info(f"Found submission: {item['data']['author']}")
            item_sub = f"https://www.reddit.com{item['data']['permalink']}"
            if item_sub == kwargs["last_sub"]:
                log.info(f"Limit reached for ticker: {kwargs['ticker']}.")
                limited = True
                return
            else:
                yield self.add_item(item["data"], kwargs["ticker"])

        if after and not limited:
            payload: dict = {
                "q": f"${kwargs['ticker']}",
                "limit": 1000,
                "after": after,
                "sort": "new",
                "t": "all",
            }

            yield Request(
                url=f"https://oauth.reddit.com/search.json?{urlencode(payload)}",
                headers=self.headers,
                callback=self.parse_search_result,
                cb_kwargs={"ticker": kwargs["ticker"], "last_sub": kwargs["last_sub"]},
            )
