"""Accesswire articles spider."""
from datetime import timezone
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import CLAUDIO
from agblox.spiders.helpers import BaseSpider
import dateutil
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader


log = logging.getLogger(__name__)


class AccesswireSpider(BaseSpider):
    """Spider for the accesswire.com site."""

    name: str = "accesswire.com"
    url: str = "https://www.accesswire.com/users/api/newsroom?skipthis=0"
    tags: List[str] = ["article", "accesswire.com"]
    host_header = "www.accesswire.com"
    spider_author = CLAUDIO

    current_page = 0  # latest page loaded from the news API
    article_requests = 0  # count number of article requests sent

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse front page with the list of articles.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        data = response.json()
        title = data["data"].get("title")

        self.total = int(data["count"])

        if title != "Latest News":
            raise Exception(
                f"Unexpected title field in data returned\n"
                f"was expecting Latest News\n"
                f"actually received {title}\n"
            )

        for a in data["data"]["articles"]:
            self.article_requests += 1
            yield scrapy.Request(a["releaseurl"], callback=self.parse_article)

            if self.last_url and a["releaseurl"] in self.last_url:
                log.info("Last URL was reached.")
                return

        if self.article_requests >= self.total:
            log.info(f"Last page reached: index={self.current_page})")
            return

        self.current_page += 1
        new_page = f"https://www.accesswire.com/users/api/newsroom?skipthis={self.current_page}"

        if self.last_url and new_page in self.last_url:
            log.info("Last URL was reached.")
            return

        yield scrapy.Request(new_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=ArticleItem(), response=response)

        loader.add_value("author", self.name)

        date = response.xpath('//div[@id="date"]/text()').get()
        iso_date = dateutil.parser.parse(date).replace(tzinfo=timezone.utc)

        loader.add_value("created_at", str(iso_date))

        """loader.add_xpath("created_at", '//div[@id="date"]/text()')"""

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", '//div[@id="articleBody"]//text()')

        loader.add_xpath("title", '//h1[@id="articleHeading"]/text()')

        loader.add_value("url", response.url)

        yield loader.load_item()
