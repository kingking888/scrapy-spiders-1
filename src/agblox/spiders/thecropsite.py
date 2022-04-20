"""Articles spider."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import ARKADY
from agblox.spiders.helpers import BaseSpider
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class ThecropsiteSpider(BaseSpider):
    """Spider for thecropsite.com site."""

    name: str = "thecropsite.com"
    url: str = "https://www.thecropsite.com/news/category/61/wheat/"
    tags: List[str] = ["article", "thecropsite.com"]
    host_header = "thecropsite.com"
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//div[@class='newsIndexItem']/a/@href"):
            if self.last_url and article in self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        next_page = etree.xpath("//div[@id='pageNext']/a/@href")
        if next_page:
            yield scrapy.Request(next_page[0], callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        loader = ItemLoader(item=ArticleItem(), response=response, date_format="DD MMMM YYYY")

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", "//span[@class='newsdate']/text()")

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath("text", "//div[@id='articles1']//*[normalize-space(text())]/text()")

        loader.add_xpath(
            "title", "//h2[@class='newsArticlesTitle' or " "@class='newsArticlesTitleImage']/text()"
        )

        loader.add_value("url", response.url)

        yield loader.load_item()
