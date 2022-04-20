"""Articles spider."""

from json.decoder import JSONDecodeError
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import ARKADY
from agblox.spiders.helpers import BaseSpider
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from scrapy.settings import Settings

log = logging.getLogger(__name__)


class ReutersSpider(BaseSpider):
    """Base spider for reuters.com site."""

    name: str = "reuters.com"
    host_header: str = "www.reuters.com"
    url: str = (
        "https://wireapi.reuters.com/v7/feed/url/www.reuters.com/markets/agriculture?until={until}"
    )
    tags: List[str] = ["article", "reuters.com"]
    spider_author = ARKADY

    @classmethod
    def update_settings(cls, settings: Settings) -> None:
        """Customize spider settings."""
        cls.custom_settings["DEFAULT_REQUEST_HEADERS"] = {"user-agent": cls.user_agent}
        cls.custom_settings["DOWNLOAD_DELAY"] = cls.download_delay
        settings.setdict(cls.custom_settings or {}, priority="spider")

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        self.get_last_url()
        url = self.url.format(until=0)  # newest page
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        try:
            body = response.json()
        except JSONDecodeError:
            log.warning(f"Unable to get json body for: {response.url}")
            return
        articles = body["wireitems"]
        if not articles:
            return

        for article in articles:
            if article["wireitem_type"] != "story":
                continue
            url = article["templates"][1]["template_action"]["url"]
            if url == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(url, callback=self.parse_article)

        # that is the trick because sometimes site returns last ID to early
        index = -2 if len(articles) > 1 else -1
        last_article_id = articles[index]["wireitem_id"]

        next_page = self.url.format(until=last_article_id)
        yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")

        loader = ItemLoader(item=ArticleItem(), response=response)
        loader.add_value("author", self.name)
        loader.add_xpath("created_at", "//meta[@property='og:article:published_time']/@content")
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", "//div[@class='ArticleBodyWrapper']/p/text()")
        loader.add_xpath("title", "//meta[@property='og:title']/@content")
        loader.add_value("url", response.url)

        yield loader.load_item()
