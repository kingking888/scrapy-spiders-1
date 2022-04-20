"""Articles spider."""
import logging
from typing import Iterator, List

from agblox.items import ArticleItem
from agblox.settings import CLAUDIO
from agblox.spiders.helpers import BaseSpider
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader


log = logging.getLogger(__name__)


class ForkastSpider(BaseSpider):
    """Spider for forkast.news site."""

    name: str = "forkast.news"
    url: str = "https://forkast.news/wp-json/wp/v2/posts?per_page=100&page=1"
    tags: List[str] = ["article"]
    spider_author = CLAUDIO
    handle_httpstatus_list = [400]

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse 100 items in json output."""
        if response.status == 400:
            # closing logic here
            raise CloseSpider("Spider DONE!")
        else:
            url = str(response.url).split("&page=")
            this_page_string = url[1]
            this_page = int(this_page_string)
            next_page_number = this_page + 1
            next_page = url[0] + "&page=" + str(next_page_number)

            json_response = response.json()
            item_counter = 0
            log.info(f"{response.url}")
            total = len(json_response)
            log.info(f"Now processing {response.url} Found: {total} items")

            for article in json_response:

                link = article.get("link")
                if link == self.last_url:
                    log.info("Limit reached.")
                    return

                item_counter += 1
                idnum = article.get("id")

                loader = ItemLoader(item=ArticleItem(), response=response)
                loader.add_value("author", self.name)

                created_at = article.get("date_gmt")
                created_at = created_at + "+00:00"
                loader.add_value("created_at", created_at)

                article_text = str(article)
                loader.add_value("raw", article_text)
                loader.add_value("tags", self.tags)

                content = article.get("content")
                content_text = content["rendered"]
                loader.add_value("text", content_text)

                title = article.get("title")
                loader.add_value("title", title["rendered"])

                loader.add_value("url", link)

                log.info(f"\nItem:{item_counter} ID:{idnum} URL:{link}\n")

                yield loader.load_item()

            yield scrapy.Request(url=next_page, callback=self.parse)
