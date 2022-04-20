"""Zerohedge News Spider."""

from datetime import timezone
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import ROSS
from agblox.spiders.helpers import BaseSpider
import dateutil.parser
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class ZeroHedgeSpider(BaseSpider):
    """Spider for zerohedge.com site."""

    name: str = "zerohedge.com"
    url: str = "https://www.zerohedge.com/"
    tags: List[str] = ["article", "zerohedge.com"]
    host_header = "www.zerohedge.com"
    spider_author = ROSS

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse Navigation page."""
        for link in response.css("div.Article_nonStickyContainer__1wgF6 a::attr(href)"):
            yield response.follow(link.get(), callback=self.parse_article)

        next_page = response.css("a.SimplePaginator_next__15okP").attrib["href"]

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse Article Page."""
        loader = ItemLoader(item=ArticleItem(), response=response)
        date_str = response.css("div.ArticleFull_headerFooter__date__3T7FN::text").get()
        date = dateutil.parser.parse(date_str).replace(tzinfo=timezone.utc)
        loader.add_value("author", self.name)
        loader.add_value("created_at", date.isoformat())
        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath(
            "text",
            "//div[@class='NodeContent_body__2clki NodeBody_container__1M6aJ']/p/text()",
        )
        loader.add_css("title", "h1.ArticleFull_title__2cUI6::text")
        loader.add_value("url", response.url)

        yield loader.load_item()
