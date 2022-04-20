"""Articles spider."""
from datetime import timezone
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import CLAUDIO
from agblox.spiders.helpers import BaseSpider
import dateutil
from lxml.html import fromstring
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class TradersinsightSpider(BaseSpider):
    """Spider for tradersinsight site."""

    name: str = "tradersinsight.news"
    host_header = "www.tradersinsight.news"
    url: str = "https://www.tradersinsight.news/category/traders-insight/securities/"
    tags: List[str] = ["article", "tradersinsight.news"]
    spider_author = CLAUDIO

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)
        for article in etree.xpath('//a//h3[@class="entry-title"]/../@href'):
            if article.startswith("https://www.tradersinsight.news"):  # skip advertisements
                if article == self.last_url:
                    log.info("Limit reached.")
                    return
                yield scrapy.Request(article, callback=self.parse_article)
        try:
            next_page = etree.xpath('//a[@class="next page-numbers"]/@href')[0]
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response)

        # //div/a[@class='author url fn']/text()
        loader.add_value("author", self.name)

        date = response.xpath('//p[@class="post-date"]/em//text()').get()
        date = date[8 : len(date)]
        date = date.strip()
        # print(f"\nDATE found: {date}\n\n")
        iso_date = dateutil.parser.parse(date).replace(tzinfo=timezone.utc)
        loader.add_value("created_at", str(iso_date))

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)
        loader.add_xpath("text", '//div[@class="entry-content"]/p//text()')
        loader.add_xpath("title", "/html/head/title//text()")
        loader.add_value("url", response.url)

        yield loader.load_item()
