"""Common spiders helpers."""

from abc import ABC
import json
import logging
import os
import pathlib
from random import shuffle
from typing import Any, Dict, Iterator, List, Optional

from agblox.settings import (
    AWS_REGION,
    DATALAKE_API_PASSWORD,
    DATALAKE_API_URL,
    DATALAKE_API_USER,
    ECS_CONTAINER_METADATA_URI,
    ENVIRONMENT,
    POLYGON_ACCESS_TOKEN,
    SPIDER_AUTHORS_SLACK_IDS,
    TO_CLOUDWATCH,
)
import arrow
import attr
import boto3
import requests
from requests.auth import HTTPBasicAuth
import scrapy
from scrapy.settings import Settings
import watchtower

log = logging.getLogger(__name__)


class SpiderConfigurationError(Exception):
    """Exception which raised if configuration can't be received."""

    pass


@attr.s(auto_attribs=True)
class UserAgent:
    """Class for work with randomised user agents."""

    file: str = attr.ib(default="useragent.txt")
    headers: List[str] = attr.ib()

    @headers.default
    def get_headers(self) -> List[str]:
        """Read User agents from file and randomize order."""
        headers_file = pathlib.Path(__file__).parent.absolute() / self.file
        with headers_file.open() as f:
            s = f.read()
        headers = s.split("\n")
        shuffle(headers)
        return headers

    def get_ua(self) -> str:
        """Return new user agent header and delete it from list."""
        return self.headers.pop()


def headers(site: str) -> Dict[str, str]:
    """Non suspicious default headers."""
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": site,
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1",
    }


def media_mime_types() -> Dict:
    """Map audio MIME types with file extensions.

    Can be extended by adding new MIME types.
    Refer to: https://www.freeformatter.com/mime-types-list.html
    """
    mime_types = {
        "audio/mpeg": ".mp3",
        "video/3gpp": ".3gp",
        "audio/mpeg": ".mp3",
        "audio/mp4": ".m4a",
        "audio/x-m4a": ".m4a",
        "audio/ogg": ".ogg",
        "audio/wav": ".wav",
    }
    return mime_types


class BaseSpider(scrapy.Spider):
    """Common class for the AgBlox spiders."""

    config: Optional[str] = None
    custom_settings: Dict[str, Any] = {}
    host_header: Optional[str] = None
    last_url: Optional[str] = None
    url: Optional[str] = None
    user_agent: str = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"
    download_delay = 1
    cloud_watch_log_url = None
    spider_author: Optional[str] = None
    is_task = os.getenv("TASK", False)

    def __init__(self, *args, **kwargs) -> None:
        """CloudWatch logging handler initialization."""  # noqa: D403
        super(BaseSpider, self).__init__(*args, **kwargs)
        if TO_CLOUDWATCH:
            if not self.is_task:
                region = AWS_REGION
                log_group = f"scrapy-{ENVIRONMENT}"
                stream_name = f"{self.name}-{arrow.now().int_timestamp}"
                cw_handler = watchtower.CloudWatchLogHandler(
                    log_group=log_group,
                    log_group_retention_days=7,
                    stream_name=stream_name,
                )  # create own CW stream
                cw_handler.setLevel("INFO")
                logging.getLogger().addHandler(cw_handler)  # add our hadler to log event
            else:
                r = requests.get(
                    f"{ECS_CONTAINER_METADATA_URI}/task"
                )  # request Fargate task metadata
                log.info(r.text)
                task_meta = json.loads(r.text)
                cluster = task_meta["Cluster"].split("/")[-1]
                task = task_meta["TaskARN"].split("/")[-1]
                region = task_meta["TaskARN"].split(":")[3]
                name = task_meta["Containers"][0]["Name"]

                log_group = f"$252Faws$252Ffargate$252F{cluster}"
                stream_name = f"cron$252F{name}$252F{task}"

            log_url = (
                f"https://console.aws.amazon.com/cloudwatch/home?region={region}"
                f"#logsV2:log-groups/log-group/{log_group}/log-events/{stream_name}"
            )
            self.cloud_watch_log_url = log_url
        log.info(f"Spider author: {self.get_spider_author()}")

    @classmethod
    def get_cfg_from_file(cls) -> Dict[str, Any]:
        """Get spider configuration from file."""
        if cls.config is None:
            raise SpiderConfigurationError("No path to the configuration file.")
        cfg_file = pathlib.Path(cls.config).absolute()
        if not cfg_file.is_file():
            msg = f"{cfg_file} not found."
            log.info(msg)
            raise SpiderConfigurationError(msg)
        with cfg_file.open() as f:
            return json.load(f)

    @classmethod
    def get_cfg_from_api(cls) -> Dict[str, Any]:
        """Get spider configuration from API."""
        if not DATALAKE_API_URL:
            raise SpiderConfigurationError("No API URL provided.")
        r = requests.get(
            f"{DATALAKE_API_URL}/sources/spider-config?name={cls.name}",
            auth=HTTPBasicAuth(DATALAKE_API_USER, DATALAKE_API_PASSWORD),
        )
        if r.status_code != 200:
            log.error(r.text)
            raise SpiderConfigurationError("Can't read configuration from API")
        return r.json()

    @classmethod
    def get_cfg(cls) -> Dict[str, Any]:
        """Read spider configuration."""
        try:
            cfg = cls.get_cfg_from_file()
        except Exception as e:
            log.info(f"Can't read configuration from file for [{cls.name}]. {e}")
        else:
            return cfg
        try:
            cfg = cls.get_cfg_from_api()
        except Exception as e:
            log.info(f"Can't read configuration from API. {e}")
        else:
            return cfg
        raise SpiderConfigurationError("Can't read spider configuration.")

    @classmethod
    def update_settings(cls, settings: Settings) -> None:
        """Customize spider settings."""
        cls.custom_settings["DEFAULT_REQUEST_HEADERS"] = headers(
            cls.host_header if cls.host_header else cls.name
        )
        cls.custom_settings["DOWNLOAD_DELAY"] = cls.download_delay
        settings.setdict(cls.custom_settings or {}, priority="spider")

    @classmethod
    def from_crawler(cls, crawler: Any, *args, **kwargs) -> "BaseSpider":
        """This method is used by Scrapy to create your spiders."""
        cls.config = kwargs.get("config")
        cls.cfg = cls.get_cfg()
        crawler.cfg = cls.cfg
        exclude_config = ["twitter", "reddit.com", "yahoo-finance"]
        if crawler.spidercls.name not in exclude_config:
            meta_settings = cls.cfg["meta"]["settings"]
            settings = crawler.settings.copy()
            settings.frozen = False
            for i in meta_settings:
                for k, v in meta_settings[i].items():
                    if settings[k] is None:
                        settings[k] = "1" if v else "0"
            settings.freeze()
            crawler.settings = settings
        return super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)

    def get_last_url(self) -> None:
        """Parse config file."""
        cfg = self.cfg
        if "url" in cfg:
            self.last_url = cfg["url"]
            log.info(f"Last url: {cfg['url']}")
        else:
            raise SpiderConfigurationError(f"Malformed configuration. {cfg}")

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        self.get_last_url()
        yield scrapy.Request(url=self.url, callback=self.parse)

    def get_spider_author(self) -> str:
        """Method which returns spider's author ID if provided."""
        return SPIDER_AUTHORS_SLACK_IDS[self.spider_author]


class EquitySpider(BaseSpider):
    """Common class for equity spiders driven by list of Tickers."""

    tags: list = ["equity"]

    @classmethod
    def get_cfg_from_api(cls) -> Dict[str, Any]:
        """Get spider configuration from API."""
        if not DATALAKE_API_URL:
            raise SpiderConfigurationError("No API URL provided.")
        r = requests.get(
            f"{DATALAKE_API_URL}/sources/spider-config?name={cls.name}&is_equity=true",
            auth=HTTPBasicAuth(DATALAKE_API_USER, DATALAKE_API_PASSWORD),
        )
        if r.status_code != 200:
            log.error(r.text)
            raise SpiderConfigurationError("Can't read configuration from API")
        return r.json()

    @classmethod
    def get_tickers_from_api(cls, limit: int, sort_order: str) -> Dict[str, Any]:
        """Get tickers list from API with sort order and limit."""
        if not DATALAKE_API_URL:
            raise SpiderConfigurationError("No API URL provided.")
        r = requests.get(
            f"{DATALAKE_API_URL}/reference/tickers?limit={limit}&sort_order={sort_order}",
            auth=HTTPBasicAuth(DATALAKE_API_USER, DATALAKE_API_PASSWORD),
        )
        if r.status_code != 200:
            log.error(r.text)
            raise SpiderConfigurationError("Can't read configuration from API")
        return r.json()

    @classmethod
    def get_spider_conf_tickers(cls) -> Dict[str, Any]:
        """Get spider configuration with tickers by given spider name."""
        if not DATALAKE_API_URL:
            raise SpiderConfigurationError("No API URL provided.")
        r = requests.get(
            f"{DATALAKE_API_URL}/sources/spider-config-tickers?name={cls.name}",
            auth=HTTPBasicAuth(DATALAKE_API_USER, DATALAKE_API_PASSWORD),
        )
        if r.status_code != 200:
            log.error(r.text)
            raise SpiderConfigurationError("Can't read configuration from API")
        return r.json()

    @classmethod
    def get_last_url_for_tag(cls, tag: str) -> Dict[str, Any]:
        """Request last scraped text for given author (spider) and tag."""
        if not DATALAKE_API_URL:
            raise SpiderConfigurationError("No API URL provided.")
        r = requests.get(
            f"{DATALAKE_API_URL}/texts?tags={tag}&authors={cls.name}"
            f"&limit=1&sort_order=desc&with_count=false",
            auth=HTTPBasicAuth(DATALAKE_API_USER, DATALAKE_API_PASSWORD),
        )
        if r.status_code != 200:
            log.error(r.text)
            raise SpiderConfigurationError("Unable to obtain last scraped url for tag: %s" % tag)
        return r.json()

    @staticmethod
    def create_url(ticker: str) -> str:
        """Override to return equity specific url."""
        raise NotImplementedError

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        for ticker, value in self.cfg["meta"]["tickers"].items():
            last_url = value.get("url")
            yield scrapy.Request(
                url=self.create_url(ticker),
                callback=self.parse,
                cb_kwargs={"ticker": ticker, "last_url": last_url},
            )


class AudioSpider(BaseSpider):
    """Class for splitting audio spiders."""

    tags: List = ["audio"]


class VideoSpider(BaseSpider):
    """Class for splitting video spiders."""

    tags: List = ["video"]


class ModelDataSpider(BaseSpider):
    """Base spider using for obtaining data for models for companies.

    Added for extending purposes if will be need.
    """

    tickers_bucket = os.getenv("S3_BUCKET")

    def __init__(self, *args, **kwargs) -> None:
        """Up S3 bucket."""
        super(ModelDataSpider, self).__init__(*args, **kwargs)
        self.s3 = boto3.client("s3")

    def start_requests(self) -> Iterator[scrapy.Request]:
        """Must be implemented in child spider class."""
        raise NotImplementedError

    def fetch_tickers_from_s3(self) -> dict:
        """Fetch latest file with tickers."""
        params = {"Bucket": self.tickers_bucket, "Prefix": "companies-models-data/tickers/"}
        response = self.s3.list_objects(**params)
        objects = response["Contents"]
        latest = max(objects, key=lambda x: x["LastModified"])
        file_object = self.s3.get_object(Bucket=self.tickers_bucket, Key=latest["Key"])
        file_content = file_object["Body"].read().decode("utf-8")

        return json.loads(file_content)


class PolygonSpider(EquitySpider, ABC):
    """Spiders class for collecting data from Polygon.io API."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize basics jobs."""
        super(PolygonSpider, self).__init__(*args, **kwargs)
        self.key = POLYGON_ACCESS_TOKEN

    def start_requests(self) -> Iterator[scrapy.Request]:
        """Must be implemented in child spider class."""
        raise NotImplementedError


def update_status(payload: dict, spider_name: str) -> None:
    """Update spider run status."""
    if not DATALAKE_API_URL:
        log.info("API url not provided. Status update skipped.")
        return
    r = requests.put(
        f"{DATALAKE_API_URL}/sources/stats/{spider_name}",
        json=payload,
        auth=HTTPBasicAuth(DATALAKE_API_USER, DATALAKE_API_PASSWORD),
    )
    if r.status_code != 204:
        log.error(r.text)
