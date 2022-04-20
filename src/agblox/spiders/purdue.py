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


class PurdueSpider(BaseSpider):
    """Spider for ag.purdue.edu site."""

    name: str = "ag.purdue.edu"
    url: str = "https://ag.purdue.edu/commercialag/ageconomybarometer/category/report/"
    tags: List[str] = ["article", "ag.purdue.edu"]
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath("//h2/a/@href"):
            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = etree.xpath("//a[contains(text(),'Next ')]/@href")[0]
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        loader = ItemLoader(
            item=ArticleItem(), response=response, date_format="dddd, MMMM Do, YYYY"
        )

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", "/html/body/div[4]/div/div[2]/p[1]/em/text()")

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        text_xpath = (
            "//div[contains(@class,'maincontent')]/"
            "p[position()>2 and not(contains(@class,'has-text-align-right'))]"
            "//text()"
        )

        loader.add_xpath("text", text_xpath)

        loader.add_xpath("title", "//h1/text()")

        loader.add_value("url", response.url)

        yield loader.load_item()
