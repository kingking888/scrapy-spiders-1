"""FSR collection spiders."""

from datetime import timezone
import logging
from typing import Iterator

from agblox.items import AudioEpisodeItem
from agblox.settings import YURI
from agblox.spiders.helpers import AudioSpider, media_mime_types
import dateutil
import feedparser
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
import w3lib.html

log = logging.getLogger(__name__)


class NotFoundAudioSource(Exception):
    """Exception handler for RSS feeds with no audio source links found."""

    pass


class RSSAudioSpider(AudioSpider):
    """Generic spider for downloading audio from given RSS url."""

    spider_author = YURI
    tags = ["audio", "equity", "podcast"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 300,
            "agblox.pipelines.S3AudioPipeline": 330,
            "agblox.pipelines.FSAudioVideoPipeline": 340,
            # "agblox.pipelines.APIPipeline": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        }
    }

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse returned text response from.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        d = feedparser.parse(response.text)
        items = d["items"]
        if not items:
            d = feedparser.parse(response.url)
            items = d["items"]
        for item in items:
            loader = ItemLoader(item=AudioEpisodeItem(), response=response)
            # Implement check on link because some items does not have link and to stop fetching, its needed.
            if item.get("link"):
                if item["link"] == self.last_url:
                    log.info("Limit reached.")
                    return

            try:
                loader.add_value("title", item["title"])
                loader.add_value("author", self.name)
                loader.add_value(
                    "text",
                    "",
                )  # initially it'll be an empty string

                date = item["published"]
                parsed_date = dateutil.parser.parse(date).replace(tzinfo=timezone.utc)
                loader.add_value("created_at", str(parsed_date))

                loader.add_value("raw", str(item))
                loader.add_value("tags", self.tags)

                audio_source_url, source_type = self._get_audio_source_link(item)
                loader.add_value("url", audio_source_url)
                summary = w3lib.html.remove_tags(item["summary"])
                loader.add_value(
                    "meta",
                    {
                        "audio_data": {
                            "is_audio": True,
                            "short_description": summary,
                            "transcribe_status": "new",
                            "source_type": source_type,
                        }
                    },
                )
                yield loader.load_item()

            except NotFoundAudioSource as e:
                log.warning(e)
            except KeyError as e:
                raise CloseSpider(
                    f"Please check RSS feed items: {response.url}. Can't access key: {e} from item."
                )

        return

    def _get_audio_source_link(self, item: dict) -> str:
        """Search and return first common href with type audio/mpeg."""
        audio_links = []
        for x in item["links"]:
            if x.get("type") in media_mime_types().keys():
                href = x.get("href")
                if not href.startswith("https://"):
                    log.info(f"GOT WRONG URL: {href}")
                audio_links.append(tuple([href, x.get("type")]))
        if audio_links:
            return audio_links[0]
        else:
            raise NotFoundAudioSource(f"Not found audio source links for: {x}")
