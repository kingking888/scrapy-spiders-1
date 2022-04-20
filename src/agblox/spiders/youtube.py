"""RSS youtube collection spiders."""
import logging
from typing import Iterator, List

from agblox.items import YoutubeVideoItem
from agblox.settings import CLAUDIO
from agblox.spiders.helpers import VideoSpider
import feedparser
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class RSSyoutubeSpider(VideoSpider):
    """Generic spider for downloading youtube files from given RSS url."""

    custom_settings = {
        "ITEM_PIPELINES": {
            "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 300,
            "agblox.pipelines.S3YouTubeVideoPipeline": 330,
            "agblox.pipelines.FSAudioVideoPipeline": 340,
            # "agblox.pipelines.APIPipeline": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        }
    }
    name: str = "youtube.com"
    url: str = "https://www.youtube.com/feeds/videos.xml?channel_id=UCNuyDSNzgtdeq9K6novdljA"
    tags: List[str] = ["video", "equity", "podcast", "from_youtube"]
    host_header = "www.youtube.com"
    spider_author = CLAUDIO

    def parse(self, response: TextResponse, **kwargs) -> Iterator[scrapy.Request]:
        """Parse returned text response from.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        log.info(f"Starting {response.url}\n")
        d = feedparser.parse(response.text)
        items = d["items"]

        for item in items:
            loader = ItemLoader(item=YoutubeVideoItem(), response=response)

            channel = getattr(self, "ytchannel", "wallstreetbets")

            loader.add_value("title", item["title"])
            loader.add_value("author", self.name)

            loader.add_value("text", "")

            # parsed_date = dateutil.parser.parse(date).replace(tzinfo=timezone.utc)
            loader.add_value("created_at", item["published"])
            loader.add_value("raw", str(item))
            loader.add_value("tags", self.tags)
            loader.add_value("url", item["link"])

            loader.add_value(
                "meta",
                {
                    "audio_data": {
                        "is_audio": True,
                        "short_description": item["summary_detail"]["value"],
                        "transcribe_status": "new",
                        "ytchannel": channel,
                        "source_type": None,  # known after download
                        "duration": None,  # known after download
                    }
                },
            )

            yield loader.load_item()
