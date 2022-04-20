"""Scrapy spider module for downloading SPG and OECD data."""

from typing import Iterator

from agblox.items import ModelDataItem
from agblox.settings import YURI
from agblox.spiders.helpers import headers, ModelDataSpider
import scrapy
from scrapy.http import Response
from urllib3.util import parse_url


class GlobalDataSpider(ModelDataSpider):
    """Spider for downloading job."""

    name = "global_data"
    spider_author = YURI
    s3_dir_key = ""
    file_prefix = ""
    extension = None
    sources_map: dict = {
        "smb": (
            "https://www.spglobal.com/spdji/en/idsexport/file.xls?hostIdentifier=48190c8c-"
            "42c4-46af-8d1a-0cd5db894797&redesignExport=true&languageId=1&selectedModule=P"
            "erformanceGraphView&selectedSubModule=Graph&yearFlag=tenYearFlag&indexId=1000"
            "03084",
            "companies-models-data/smb/",
        ),
        "qual": (
            "https://www.spglobal.com/spdji/en/idsexport/file.xls?hostIdentifier=48190c8c"
            "-42c4-46af-8d1a-0cd5db894797&redesignExport=true&languageId=1&selectedModule"
            "=PerformanceGraphView&selectedSubModule=Graph&yearFlag=fiveYearFlag&indexId="
            "91920515",
            "companies-models-data/qual/",
        ),
        "mom": (
            "https://www.spglobal.com/spdji/en/idsexport/file.xls?hostIdentifier=48190c8c-"
            "42c4-46af-8d1a-0cd5db894797&redesignExport=true&languageId=1&selectedModule=P"
            "erformanceGraphView&selectedSubModule=Graph&yearFlag=fiveYearFlag&indexId=920"
            "24474",
            "companies-models-data/mom/",
        ),
        "hml": (
            "https://www.spglobal.com/spdji/en/idsexport/file.xls?hostIdentifier=48190c8c-"
            "42c4-46af-8d1a-0cd5db894797&redesignExport=true&languageId=1&selectedModule=P"
            "erformanceGraphView&selectedSubModule=Graph&yearFlag=tenYearFlag&indexId=1000"
            "03086",
            "companies-models-data/hml/",
        ),
        "oecd": (
            "https://raw.githubusercontent.com/NicolasWoloszko/OECD-Weekly-Tracker/main/"
            "Data/weekly_tracker.xlsx",
            "companies-models-data/oecd/",
        ),
    }

    custom_settings = {
        "ITEM_PIPELINES": {
            "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 300,
            # "agblox.pipelines.FSJsonPipeline": 310,  # ToDo: Check if is working
            # "scrapy.pipelines.files.FilesPipeline": 320,
            "agblox.pipelines.S3DataPipeline": 320,
            "agblox.pipelines.APIPipelineReport": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        },
    }

    def start_requests(self) -> Iterator[scrapy.Request]:
        """After the spider will be opened this method starts."""
        for k, v in self.sources_map.items():
            host_header = parse_url(v[0]).host
            custom_headers = headers(host_header)
            yield scrapy.Request(v[0], headers=custom_headers, cb_kwargs={"source": k})

    def parse(self, response: Response, **kwargs) -> Iterator[scrapy.Item]:
        """Method for handling each scrapy responce."""
        source_key = kwargs.get("source")
        self.logger.info("Fetched data for: [%s]", source_key)
        data = response.body

        self.file_prefix = f"{source_key}_"
        self.s3_dir_key = self.sources_map[source_key][1]
        self.extension = parse_url(response.url).path.split(".")[-1]

        item = ModelDataItem(data=data)
        yield item
