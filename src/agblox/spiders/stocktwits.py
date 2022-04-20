"""StockTwitsGeneric collection spiders."""

import json
import logging
from typing import Iterator

from agblox.items import EquityArticleItem
from agblox.settings import DANIEL
from agblox.spiders.helpers import EquitySpider
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class StocktwitsSpider(EquitySpider):
    """Spider for stocktwits site."""

    host_header: str = "api.stocktwits.com"
    headers: dict = {"Content-Type": "application/json"}
    name = "stocktwits.com"
    spider_author = DANIEL

    @staticmethod
    def create_url(ticker: str) -> str:
        """Override to return equity specific url."""
        base_url_prefix = "https://api.stocktwits.com/api/2/streams/symbol/"
        base_url_suffix = ".json?filter=top&limit=50"
        return f"{base_url_prefix}{ticker}{base_url_suffix}"

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        scraped_tickers = self.cfg["meta"]["tickers"]
        for ticker in scraped_tickers:
            try:
                last_url = scraped_tickers[ticker].get("url")
            except KeyError:
                last_url = None
            url = self.create_url(ticker)
            name = f"stocktwits-{ticker}"
            tags = ["social", self.name, "equity"]

            yield scrapy.Request(
                url=url,
                callback=self.parse,
                cb_kwargs={
                    "last_url": last_url,
                    "url": url,
                    "name": name,
                    "tags": tags,
                    "ticker": ticker,
                },
            )

    def parse(self, response: TextResponse, **kwargs) -> Iterator[EquityArticleItem]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        response_body = json.loads(response.body.decode("utf-8"))

        last_id = 0
        if kwargs["last_url"] and kwargs["last_url"] == response.url:
            log.info("Last URL reached.")
            return
        else:
            kwargs["last_url"] = response.url

        for message in response_body["messages"]:

            item, last_id = self.add_item(message, response, kwargs)

            if item is not None:
                yield item

        next_url = f"{kwargs['url']}&max={last_id}"

        yield scrapy.Request(url=next_url, callback=self.parse, cb_kwargs=kwargs)

    def add_item(
        self, message: dict, response: TextResponse, kwargs: dict
    ) -> (EquityArticleItem, int):
        """Method for add item to ItemLoader."""
        url = (
            "https://stocktwits.com/"
            + message["user"]["username"]
            + "/message/"
            + str(message["id"])
        )

        log.info(f"Article URL: {url}")

        try:
            loader = ItemLoader(item=EquityArticleItem(), response=response)

            loader.add_value("author", kwargs["name"])
            loader.add_value("created_at", message["created_at"])
            loader.add_value("raw", json.dumps(message))
            loader.add_value("tags", kwargs["tags"])

            meta = {
                "post_author": message["user"]["username"],
                "id": message["id"],
                "base_ticker": kwargs["ticker"],
            }

            loader.add_value("meta", meta)

            loader.add_value("text", message["body"])
            loader.add_value("title", "StockTwitsTitle")
            loader.add_value("url", url)

            return loader.load_item(), message["id"]

        except Exception:

            log.error(f"Found problem with: {url}", exc_info=True)
            return None
