"""Penn State Exception report collection spiders."""
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


class PennStateSpider(BaseSpider):
    """Spider for Penn State articles."""

    name: str = "extension.psu.edu"
    url: str = "https://extension.psu.edu/shopby/articles?limit=50&mode=list&p=1"
    tags: List[str] = ["article", "extension.psu.edu"]
    host_header = "extension.psu.edu"
    spider_author = ARKADY

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Function used to individual article urls out of all landing pages."""
        etree = fromstring(response.text)
        etree.make_links_absolute(response.url)

        for article in etree.xpath('//div[@class="item"]/div[@class="item-inner clearer"]/a/@href'):

            if article == self.last_url:
                log.info("Limit reached.")
                return
            yield scrapy.Request(article, callback=self.parse_article)

        next_page = etree.xpath('//a[@class="next i-next"]/@href')

        if not next_page:
            return
        else:
            yield scrapy.Request(url=next_page[0], callback=self.parse)

    def parse_article(self, response: TextResponse, **kwargs) -> Iterator[ArticleItem]:
        """Parse article page."""
        log.info(f"Article URL: {response.url}")
        loader = ItemLoader(item=ArticleItem(), response=response, date_format="MMMM D, YYYY")

        loader.add_value("author", self.name)

        loader.add_xpath("created_at", '//meta[@itemprop="dateModified"]/@content')

        loader.add_value("raw", response.text)
        loader.add_value("tags", self.tags)

        loader.add_xpath(
            "text",
            '//div[@itemprop="articleBody" and not(@class = "discreet")]'
            "//*[normalize-space(text())]//text()",
        )

        loader.add_xpath("title", '//h1[@itemprop="headline"]/text()')

        loader.add_value("url", response.url)

        yield loader.load_item()
