"""Intrinio Quarter Spider."""
import datetime
import json
import logging
from typing import Iterator

from agblox.settings import AZKA, INTRINIO_API_KEY
from agblox.spiders.helpers import ModelDataSpider
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import Response

log = logging.getLogger(__name__)


class IntrinioQuarterSpider(ModelDataSpider):
    """Spider for intrinio quarterly data."""

    host_header = "intrinio-bulk-downloads.s3.amazonaws.com"
    spider_author = AZKA
    name: str = "intrinio_quarter"
    api_url: str = "https://api-v2.intrinio.com/bulk_downloads"
    s3_dir_key = "companies-models-data/"
    headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}

    custom_settings = {
        "ITEM_PIPELINES": {
            "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 300,
            "agblox.pipelines.FSDataPipeline": 310,
            "agblox.pipelines.S3MultipartPipeline": 320,
            "agblox.pipelines.APIPipelineReport": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        },
    }

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping.

        We use it to obtain bulk-downloads api response.
        """
        yield scrapy.Request(
            url=f"{self.api_url}/links?api_key={INTRINIO_API_KEY}",
            callback=self.parse,
        )

    def parse(self, response: Response, **kwargs) -> scrapy.Request:
        """Parse returned response from bulk downloads api.

        Then make a request to gather companies data.
        """
        if response.status != 200:
            raise CloseSpider(response.body)

        bulk_downloads = json.loads(response.text)["bulk_downloads"]

        to_download = {
            "us-indu-calc": bulk_downloads[0]["links"][5]["url"],
            # "US_INDU_CALCULATIONS_KEY": "companies-models-data/us-indu-calc-key/",
            "us-fin-calc": bulk_downloads[0]["links"][1]["url"],
            "companies": bulk_downloads[1]["links"][0]["url"],
        }

        # Urls will be processed in pipeline with requests, chunked
        # because we have 512 Mb RAM limit in Fargate task
        for k, v in to_download.items():
            current_datetime = datetime.datetime.now()
            yield {
                "source": k,
                "s3_key": f"{self.s3_dir_key}{k}/{k}_{current_datetime.isoformat()}.gz",
                "url": v,
            }
