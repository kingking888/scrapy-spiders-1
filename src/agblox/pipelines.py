"""Item pipelines.

References:
    https://docs.scrapy.org/en/latest/topics/item-pipeline.html
"""
from base64 import b64encode
import csv
import datetime
from distutils.util import strtobool
import gzip
import hashlib
import io
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote

from agblox.items import (
    ArticleItem,
    AudioEpisodeItem,
    EquityArticleItem,
    GoogleTrendsItem,
    RedditCommentsItem,
    RedditSearchItem,
    RedditSubredditItem,
    TickerItem,
    TweetItem,
    YoutubeVideoItem,
)
from agblox.settings import (
    AWS_REGION,
    DATALAKE_API_PASSWORD,
    DATALAKE_API_URL,
    DATALAKE_API_USER,
    ENVIRONMENT,
    MODELS_API_PASSWORD,
    MODELS_API_URL,
    MODELS_API_USER,
    NOTIFIER_ARN,
    S3_BUCKET,
    SPIDER_AUTHORS_SLACK_IDS,
    YURI,
)
from agblox.spiders.helpers import media_mime_types, update_status
import arrow
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.errorfactory import ClientError
from itemadapter import ItemAdapter
from langdetect import detect, LangDetectException
import pandas as pd
from pytube import Stream, YouTube
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import InvalidSchema
from requests.packages.urllib3.util.retry import Retry
from scrapy.core.downloader import Slot
from scrapy.exceptions import DropItem
import scrapy.statscollectors
import yaml

log = logging.getLogger(__name__)


# The following block is responsible for retries in requests library
requests_retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "PUT"],
)
adapter = HTTPAdapter(max_retries=requests_retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)
# END


def get_extension(content_type: str) -> str:
    """Defines file extension based on content type.

    Args:
        content_type: A mime type of content
        https://docs.w3cub.com/http/basics_of_http/mime_types/complete_list_of_mime_types

    Returns:
        File extension string
    """
    try:
        return media_mime_types()[content_type]
    except KeyError:
        raise


class UndefinedContentType(Exception):
    """Error handler for content type undefined errors."""

    pass


def url_to_file_name(url: str, file_ext: str) -> str:
    """Convert url to the file name.

    >>> url_to_file_name(
    ...    "https://agfax.com/2020/10/08/dtn-grain-open-markets-press-higher-in-early-trade/", "mp3"
    ... )
    'agfax.com_2020_10_08_dtn-grain-open-markets-press-higher-in-early-trade_.mp3'
    """
    s = url.replace("https://", "").replace("/", "_")
    return f"{quote(s, '')}.{file_ext}"


def url_to_av_file_path(url: str, content_type: str) -> Tuple:
    """Convert url to the audio file name.

    >>> url_to_av_file_path(
    ...    "https://MyWallSt.podbean.com/e/how-has-robinhood-impacted-the-financial-markets/", "audio/mpeg"
    ... )
    ('26b50fa5cef3bc323114fdf656e4b7f7256f1af0b7389348849f539a69007594', '.mp3')
    """
    extension = get_extension(content_type)
    s = hashsum(url)
    return (f"{s}", f"{extension}")


def item_to_yml(item: scrapy.Item) -> str:
    """Convert scrapy item to yaml file."""
    return yaml.dump(dict(item), allow_unicode=True)


def item_to_json(item: scrapy.Item) -> str:
    """Convert scrapy item to json file."""
    return json.dumps(dict(item))


def bucket_key(spider_name: str, item: scrapy.Item) -> str:
    """Generate S3 bucket key."""
    return f"{spider_name}/{url_to_file_name(item['url'], 'yml')}"


def bucket_key_av(
    dir_name: str, hashsum: str, file_name: str, file_ext: str, av: str = "audios"
) -> str:
    """Generate S3 bucket key for audio and video sources."""
    return f"{av}/{dir_name}/{hashsum}/{file_name}{file_ext}"


def hashsum(s: str) -> str:
    """Converts string URL to 32 bytes/256 bit hashsum."""
    return hashlib.sha256(s.encode()).hexdigest()


def build_headers(user: str, pwd: str) -> Dict[str, str]:
    """Build API header with Basic auth.

    >>> build_headers('user', 'password')['Authorization']
    'Basic dXNlcjpwYXNzd29yZA=='
    """
    return {
        "Content-Type": "application/json",
        "Authorization": f"Basic {b64encode(f'{user}:{pwd}'.encode()).decode()}",
    }


def get_source_name(spider: scrapy.Spider) -> str:
    """Provides src dir for the reddit.stocks.search spider.

    We have 2 spiders for Reddit
     - reddit.com
     - reddit.stocks.search
    For storing posts in the same dir for both we were boud a path to spider's name here
    """
    return "reddit.com" if spider.name == "reddit.stocks.search" else spider.name


def download(url: str, path: Path, **kwargs) -> None:
    """Download file using requests library and store into file_path specified.

    Args:
        url (str): file origin
        path (Path): local path to store the file

    Returns:
        name: complete path to the file in a str type
        files_dir: path to the files directory
    """
    log.info("Downloading %s" % url)
    try:
        with http.get(url, stream=True) as r:
            r.raise_for_status()
            content_type = r.headers.get("content-type")
            audio_dir, audio_file_extension = url_to_av_file_path(url, content_type)
            files_dir = path / audio_dir
            files_dir.mkdir(parents=True, exist_ok=True)
            name = path / audio_dir / f"audio{audio_file_extension}"
            with open(name, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        log.info("Done")
        meta = {"duration": None, "content_type": content_type}
        return (name, files_dir, meta)
    except InvalidSchema:
        raise


def download_youtube(url: str, path: Path, audio_only: bool = True) -> tuple:
    """Download youtube link with pytube into file_path specified.

    Args:
        url (str): file origin
        path (Path): local path to store the file
        audio_only (bool): download audio only setting

    Returns:
        name: complete path to the file in a str type
        files_dir: path to the files directory
        meta: metadata for downloaded file
    """
    log.info(f"Downloading youtube {url}")
    try:
        yt = YouTube(url)
        duration = yt.length
        audio_stream = yt.streams.get_audio_only()
        content_type = audio_stream.mime_type
        file_dir, file_extension = url_to_av_file_path(url, content_type)
        files_dir = path / file_dir
        files_dir.mkdir(parents=True, exist_ok=True)
        name = path / file_dir / f"audio{file_extension}"
        audio_stream.download(filename=name)
        log.info("Done youtube download AUDIO_STREAM: %s" % url)
        meta = {"duration": duration, "content_type": content_type}
        if not audio_only:
            video_stream = yt.streams.first()
            vide_stream_content_type = video_stream.mime_type
            file_dir, file_extension = url_to_av_file_path(url, vide_stream_content_type)
            video_file_name = path / file_dir / f"video{file_extension}"
            video_stream.download(filename=video_file_name)
            log.info("Done youtube download VIDEO_STREAM: %s" % url)
        return name, files_dir, meta
    except Exception as e:
        log.exception("Unexpected error with youtube downloader. Error: %s" % e)


class PipelineSettingsMixin:
    """Mixin for pipeline configuration based on settings status after crawler was created."""

    SETTINGS_KEY: str = None
    active = None

    @classmethod
    def set_settings_val(cls, crawler: Any) -> None:
        """This is the class method used by this mixin to reassign settings values."""
        cls.active = crawler.settings[cls.SETTINGS_KEY]


class FSPipeline(PipelineSettingsMixin):
    """Store items to the local file system."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_FILE"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        try:
            if self.path and strtobool(self.active):
                name = self.path / url_to_file_name(item["url"], "yml")
                item["src"] = str(name)
                with name.open("w", encoding="utf-8") as f:
                    f.write(item_to_yml(item))
        except Exception:
            log.exception("Unexpected error")
        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            root = Path(__file__).parent.parent.absolute()
            self.path = root / "data" / get_source_name(spider)
            self.path.mkdir(parents=True, exist_ok=True)
            log.info(f"Data will be stored to the {self.path} folder")

    @classmethod
    def from_crawler(cls, crawler: Any) -> "FSPipeline":
        """This is the class method used by Scrapy to create pipeline class instance."""
        cls.set_settings_val(crawler)
        return cls()


class FSAudioVideoPipeline(FSPipeline):
    """Store items to the local file system."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_FILE"
    keep_video: bool = False
    meta_root = "audio_data"  # data for audio are use by default
    fs_url_key = "audio_fs_url"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        adapter = ItemAdapter(item)
        try:
            if self.path and strtobool(self.active):
                source_url = item["url"]

                file_path, files_dir, metadata = self.file_downloader(
                    url=source_url, path=self.path, audio_only=False if self.keep_video else True
                )

                if adapter.get("meta"):  # modify the item meta field
                    item["meta"][self.meta_root].update({self.fs_url_key: str(file_path)})
                    item["meta"][self.meta_root].update({"duration": metadata.get("duration")})
                    item["meta"][self.meta_root].update(
                        {"source_type": metadata.get("content_type")}
                    )

                name = files_dir / "meta.json"
                item["src"] = str(name)

                with name.open("w") as f:  # save source page file
                    f.write(item_to_json(item))
        except InvalidSchema as e:
            log.warning(f"It might be a worng redirection was used. Error: {e}. We are passing it.")
        except Exception as e:
            log.exception(f"Unexpected error: {e}")
        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            root = Path(__file__).parent.parent.absolute()
            self.path = root / "data" / get_source_name(spider)
            self.path.mkdir(parents=True, exist_ok=True)
            log.info(f"Audio and page source files will be stored to the {self.path} folder")
        if spider.name == "youtube.com":
            self.file_downloader = download_youtube
            self.meta_root = "audio_data"
            self.fs_url_key = "video_fs_url"
        else:
            self.file_downloader = download

    @classmethod
    def from_crawler(cls, crawler: Any) -> "FSAudioVideoPipeline":
        """This is the class method used by Scrapy to create pipeline class instance."""
        cls.set_settings_val(crawler)
        keep_video = crawler.settings["KEEP_VIDEO"]
        cls.keep_video = strtobool(keep_video) if keep_video else False
        return cls()


class FSCommentsPipeline(FSPipeline):
    """Modify existing source file and append comments messages."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_FILE"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        try:
            if self.path and strtobool(self.active):
                name = self.path / url_to_file_name(item["url"], "yml")
                with open(name, "r") as f:
                    source_data = yaml.safe_load(f)
                comments_data = dict(item)
                source_data["text"] += f"\n{comments_data['comments_text']}"
                source_data["meta"]["reddit_data"]["last_comment_id"] = comments_data[
                    "last_comment_id"
                ]
                with open(name, "w") as f:
                    f.write(yaml.dump(source_data))

        except Exception:
            log.exception("Unexpected error")
        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            root = Path(__file__).parent.parent.absolute()
            self.path = root / "data" / "reddit.com"
            self.path.mkdir(parents=True, exist_ok=True)
            log.info(f"Data will be stored to the {self.path} folder")


class FSModelDataPipeline(FSPipeline, PipelineSettingsMixin):
    """Store Companies Model data items to the local file system."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_FILE"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        try:
            if self.path and strtobool(self.active):
                current_datetime = datetime.datetime.now()
                name = self.path / f"tickers_{current_datetime.isoformat()}.json"
                with name.open("w", encoding="utf-8") as f:
                    f.write(json.dumps(item["data"]))
        except Exception:
            log.exception("Unexpected error")
        return item


class FSCSVPipeline(FSPipeline, PipelineSettingsMixin):
    """Pipeline for storing CSV file from Pandas Data frame."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_FILE"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """Process scraped item based on conditions."""
        frame = pd.DataFrame(item["data"])
        try:
            if self.path and strtobool(self.active):
                current_datetime = datetime.datetime.now()
                name = self.path / f"{spider.file_prefix}_{current_datetime.isoformat()}.csv"
                frame.to_csv(name, index=False)
        except Exception:
            log.exception("Unexpected error")
        return item


class CSVPipeline(FSPipeline, PipelineSettingsMixin):
    """Pipeline for storing CSV file from Pandas Data frame."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_FILE"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """Process scraped item based on conditions."""
        try:
            if self.path and strtobool(self.active):
                row = ItemAdapter(item).asdict()
                self.writer.writerow(row)
        except Exception:
            log.exception("Unexpected error")
        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """Called on spider start."""
        super(CSVPipeline, self).open_spider(spider)
        if self.path and strtobool(self.active):
            self.csvfile = open(
                self.path / f"{spider.__getattribute__('csv_filename')}.csv", "w", newline=""
            )
            self.writer = csv.DictWriter(
                self.csvfile, fieldnames=spider.__getattribute__("csv_fieldnames")
            )
            self.writer.writeheader()

    def close_spider(self, spider: scrapy.Spider) -> None:
        """Called on spider stop."""
        if strtobool(self.active):
            self.csvfile.close()


class FinCalendarsPipeline(FSPipeline, PipelineSettingsMixin):
    """Pipeline for fin_calendars spider."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_FILE"

    def __init__(self) -> None:
        """Initialize pandas data frame."""
        self.frame = pd.DataFrame()
        self.symbols = []

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """Process scraped item based on conditions."""
        if "historical" in json.loads(item["data"][0]):
            self.frame = pd.concat(
                [self.frame, pd.json_normalize(json.loads(item["data"][0])["historical"])]
            )
            self.symbols.extend(
                item["ticker"] * len(pd.json_normalize(json.loads(item["data"][0])["historical"]))
            )
        else:
            self.frame = pd.concat([self.frame, pd.read_json(item["data"][0])])
        return item

    def close_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is closed."""
        log.info(f"Spider {spider.name} closed")
        self.frame = self.frame.reset_index()
        if spider.name == "dividends_calendars":
            self.frame["symbol"] = self.symbols
        try:
            if self.path and strtobool(self.active):
                current_datetime = datetime.datetime.now()
                name = (
                    self.path
                    / f"{spider.__getattribute__('file_prefix')}{current_datetime.isoformat()}.csv"
                )
                self.frame.to_csv(name)
        except Exception:
            log.exception("Unexpected error")


class FredMacroFSPipeline(FSPipeline, PipelineSettingsMixin):
    """Pipeline for fin_calendars spider."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_FILE"

    def __init__(self) -> None:
        """Initialize pandas data frame."""
        self.frame = pd.DataFrame()
        self.k = 0

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """Process scraped item based on conditions."""
        data = item["data"]
        macro = item["ticker"]

        x = pd.DataFrame(data.reset_index().rename(columns={"index": "Date", 0: macro}))
        x = x.loc[(x.Date >= "2013-01-01")]
        x["Date"] = pd.to_datetime(x["Date"])
        x[macro] = x[macro].astype(float)
        if self.k == 0:
            self.frame["Date"] = x["Date"]
            self.frame["Date"] = pd.to_datetime(x["Date"])
            self.frame[macro] = list(x[macro])
            self.k += 1
        else:
            self.frame = pd.merge(self.frame, x, on=["Date"], how="left")

        return item

    def close_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is closed."""
        log.info(f"Spider {spider.name} closed")
        try:
            if self.path and strtobool(self.active):
                current_datetime = datetime.datetime.now()
                name = (
                    self.path
                    / f"{spider.__getattribute__('file_prefix')}{current_datetime.isoformat()}.csv"
                )
                self.frame.to_csv(name)
        except Exception:
            log.exception("Unexpected error")


class FSIntrinioDataPipeline(FSPipeline, PipelineSettingsMixin):
    """Store Companies Model data items to the local file system."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_FILE"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        data = item.get("data")
        ticker = item.get("ticker")
        try:
            if self.path and strtobool(self.active):
                encoded = json.dumps(data).encode("utf-8")
                b = io.BytesIO(encoded)
                current_datetime = datetime.datetime.now()
                ticker_dir = self.path / f"{ticker}"
                ticker_dir.mkdir(parents=True, exist_ok=True)
                name = (
                    self.path
                    / f"{ticker}"
                    / f"{ticker}_{current_datetime.isoformat().replace(':', '_')}.json"
                )
                with open(name, "w+b") as f:
                    f.write(b.read())
                log.info("Data for %s were saved locally." % item.get("ticker"))
        except Exception:
            log.exception("Unexpected error")

        return item


class FSDataPipeline(FSPipeline, PipelineSettingsMixin):
    """Store Companies Model data items to the local file system."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_FILE"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        csv_data = item.get("data")
        try:
            if self.path and strtobool(self.active):
                current_datetime = datetime.datetime.now()
                name = (
                    self.path / f"{spider.__getattribute__('file_prefix')}"
                    f"{current_datetime.isoformat().replace(':', '_')}.csv"
                )
                with open(name, "w") as f:
                    writer = csv.writer(f)
                    writer.writerows(csv_data)
        except Exception:
            log.exception("Unexpected error")
        return item


class S3Pipeline(PipelineSettingsMixin):
    """Store items to the S3 bucket."""

    s3 = None
    SETTINGS_KEY = "TO_S3"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        try:
            if self.s3:
                key = bucket_key(get_source_name(spider), item)
                item["src"] = key
                self.s3.Object(key=key).put(Body=item_to_yml(item))
        except Exception:
            log.exception("Unexpected error")
        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            self.s3 = boto3.resource("s3").Bucket(S3_BUCKET)
            log.info(
                f"Data will be stored to the S3 bucket {S3_BUCKET} Root key: {get_source_name(spider)}",
            )

    @classmethod
    def from_crawler(cls, crawler: Any) -> "S3Pipeline":
        """This is the class method used by Scrapy to create pipeline class instance."""
        cls.set_settings_val(crawler)
        return cls()


class S3AudioPipeline(S3Pipeline):
    """Store items to the S3 bucket."""

    path: Optional[Path] = None
    s3 = None
    SETTINGS_KEY = "TO_S3"
    s3_url_prefix = None

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        adapter = ItemAdapter(item)
        try:
            if self.s3:
                audio_source_url = item["url"]
                audio_source_type = item["meta"]["audio_data"]["source_type"]
                audio_id, file_ext = url_to_av_file_path(audio_source_url, audio_source_type)

                json_key = bucket_key_av(
                    get_source_name(spider), audio_id, file_name="meta", file_ext=".json"
                )
                audio_key = bucket_key_av(
                    get_source_name(spider), audio_id, file_name="audio", file_ext=file_ext
                )
                s3 = boto3.client("s3")
                try:
                    s3.head_object(Bucket=S3_BUCKET, Key=audio_key)
                    log.info(f"{audio_source_url} with key {audio_key} skipped as existed")
                except ClientError:
                    # Not found
                    if adapter.get("meta"):  # modify the item meta field
                        adapter["meta"]["audio_data"].update(
                            {"audio_s3_url": f"{self.s3_url_prefix}{audio_key}"}
                        )
                    if not adapter.get("src"):  # modify the item src field
                        adapter["src"] = f"{self.s3_url_prefix}{json_key}"

                    log.info(f"Uploading audio meta.json data to S3 bucket. Key: {json_key}")
                    self.s3.Object(key=json_key).put(Body=item_to_json(item))

                    try:
                        with http.get(audio_source_url, stream=True, allow_redirects=True) as r:
                            log.info(f"Downloading to the stream: {audio_source_url}")

                            r.raw.decode_content = True
                            conf = TransferConfig(multipart_threshold=62500, max_concurrency=4)
                            self.s3.Object(key=audio_key).upload_fileobj(r.raw, Config=conf)
                            log.info(f"DONE: Uploaded stream to S3 bucket. Key: {audio_key}")
                    except InvalidSchema as e:
                        log.warning(
                            f"It might be a worng redirection was used. Error: {e}. We are passing it."
                        )

        except Exception as e:
            log.exception(f"Unexpected error {e}")
        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            self.s3 = boto3.resource("s3").Bucket(S3_BUCKET)
            log.info(
                f"Audio and page source files will be streamed directly to the S3 bucket {S3_BUCKET}. "
                f"Root key: {get_source_name(spider)}\n"
            )
            if self.s3:
                self.s3_url_prefix = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/"

    @classmethod
    def from_crawler(cls, crawler: Any) -> "S3AudioPipeline":
        """This is the class method used by Scrapy to create pipeline class instance."""
        cls.set_settings_val(crawler)
        return cls()


class S3YouTubeVideoPipeline(S3Pipeline):
    """Store items to the S3 bucket."""

    path: Optional[Path] = None
    s3 = None
    SETTINGS_KEY = "TO_S3"
    s3_url_prefix = None

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        adapter = ItemAdapter(item)
        try:
            if self.s3:
                url = item["url"]
                self.ytchannel = item["meta"]["audio_data"]["ytchannel"]

                streams = self.modify_item(self.get_yt_streams(url), adapter)

                try:
                    json_file_key = streams[0]["stream_data"][1]
                except (IndexError, KeyError):
                    log.warning(
                        "Looks like no data or Live content from %s. YouTube channel: %s"
                        % (url, self.ytchannel)
                    )
                else:

                    if not self.obj_s3_exists(json_file_key):

                        for stream in streams:
                            self.upload_stream(stream["stream"], stream["stream_data"][0][2])
                        log.info(
                            "Uploading audio meta.json data to S3 bucket. Key: %s" % json_file_key
                        )
                        self.s3.Object(key=json_file_key).put(Body=item_to_json(item))

        except Exception as e:
            log.exception(f"Unexpected error {e}")
        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            self.s3 = boto3.resource("s3").Bucket(S3_BUCKET)
            log.info(
                f"Audio and page source files will be streamed directly to the S3 bucket {S3_BUCKET}. "
                f"Root key: {get_source_name(spider)}\n"
            )
            if self.s3:
                self.s3_url_prefix = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/"

        if spider.name == "youtube.com":
            self.file_downloader = download_youtube
            self.meta_root = "audio_data"
            self.fs_url_key = "video_fs_url"
        else:
            self.file_downloader = download

    @classmethod
    def from_crawler(cls, crawler: Any) -> "S3AudioPipeline":
        """This is the class method used by Scrapy to create pipeline class instance."""
        cls.set_settings_val(crawler)
        keep_video = crawler.settings["KEEP_VIDEO"]
        cls.keep_video = strtobool(keep_video) if keep_video else False
        return cls()

    def get_yt_streams(self, url: str) -> List:
        """Downloads needed streams with Pytube and packs needed data.

        Args:
            url: YouTube video URL

        Returns:
            list of streams
        """
        streams = []
        yt = YouTube(url)
        vid_info = yt.vid_info
        if not vid_info["videoDetails"]["isLiveContent"]:
            audio_stream = yt.streams.get_audio_only()
            # TODO: might be tuned to get audio stream by quality
            streams.extend(
                [
                    {
                        "stream": audio_stream,
                        "stream_data": self.build_keys(url, audio_stream, self.ytchannel),
                        "audio_mime_type": audio_stream.mime_type,
                        "duration": yt.length,
                    }
                ]
            )
            if self.keep_video:
                video_stream = yt.streams.first()
                # TODO: might be tuned to get video stream by quality
                streams.extend(
                    [
                        {
                            "stream": video_stream,
                            "stream_data": self.build_keys(url, video_stream, self.ytchannel),
                            "video_mime_type": video_stream.mime_type,
                        }
                    ]
                )

        return streams

    def modify_item(self, streams: List, adapter: ItemAdapter) -> List:
        """Modifies scrapy item parameters.

        Args:
            streams: list of streams with data
            adapter: scrapy item adapter

        Returns:
            list of streams
        """
        try:
            json_file_key = streams[0]["stream_data"][1]
        except IndexError:
            log.info("No streams to proceed.")
        else:

            try:
                video_stream_key = streams[1]["stream_data"][0][2]
            except (KeyError, IndexError):
                video_stream_key = None

            if adapter.get("meta"):  # modify the item meta field
                adapter["meta"]["audio_data"].update(
                    {
                        "audio_s3_url": f"{self.s3_url_prefix}{streams[0]['stream_data'][0][2]}",
                        "duration": streams[0]["duration"],
                        "audio_mime_type": streams[0]["audio_mime_type"],
                        "source_type": "video",
                    }
                )
                if video_stream_key:
                    adapter["meta"]["audio_data"].update(
                        {
                            "video_s3_url": f"{self.s3_url_prefix}{video_stream_key}",
                            "video_mime_type": streams[1]["video_mime_type"],
                        }
                    )

                if not adapter.get("src"):  # modify the item src field
                    adapter["src"] = f"{self.s3_url_prefix}{json_file_key}"
        return streams

    def build_keys(self, url: str, stream: Stream, ytchannel: str) -> [List, str]:
        """Builds filepath keys for storing files on s3.

        Args:
            url: source youtube video URL
            stream: downloaded stream object (audio or video)
            ytchannel: youtube channel from where all downloaded

        Returns:
             object with all streams data
             key for metadata json file for storing on s3
        """
        data = []

        file_dir, file_extension = url_to_av_file_path(url, stream.mime_type)
        stream_type = "video" if stream.type == "video" else "audio"
        file_key = bucket_key_av(
            ytchannel,
            file_dir,
            file_name=stream_type,
            file_ext=file_extension,
            av="audios",  # hardcoded to keep audio and video together and in 'audios' dir
        )
        data.extend((file_dir, file_extension, file_key))
        json_file_key = bucket_key_av(
            ytchannel, data[0], file_name="meta", file_ext=".json", av="audios"
        )
        return data, json_file_key

    def obj_s3_exists(self, obj_key: str) -> bool:
        """Checks if an object exists on s3 bucket.

        Now we are check on a meta.json file only existance.

        Args:
            obj_key: key to search on s3 bucker

        Returns:
            bool
        """
        s3 = boto3.client("s3")
        try:
            s3.head_object(Bucket=S3_BUCKET, Key=obj_key)
            log.info("S3 object with key %s exists" % obj_key)
            return True
        except ClientError:
            return False

    def upload_stream(self, stream: Stream, obj_key: str) -> None:
        """Uploads given stream to an s3 bucket.

        Args:
            stream: a stream object
            obj_key: filepath key to store on s3
        """
        output = io.BytesIO()
        stream.stream_to_buffer(output)
        output.seek(0)  # return cursor to the start; if no - all files will be empty
        conf = TransferConfig(multipart_threshold=62500, max_concurrency=4)
        self.s3.Object(key=obj_key).upload_fileobj(output, Config=conf)
        output.close()
        log.info(f"DONE: Uploaded {stream.type} stream to S3 bucket. Key: {obj_key}")


class S3CommentsPipeline(S3Pipeline):
    """Modify item on S3 bucket."""

    s3 = None
    SETTINGS_KEY = "TO_S3"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        try:
            if self.s3:
                key = bucket_key("reddit.com", item)
                obj = self.s3.Object(key=key).get()
                source_data = yaml.safe_load(obj["Body"])

                comments_data = dict(item)
                source_data["text"] += f"\n{comments_data['comments_text']}"
                source_data["meta"]["reddit_data"]["last_comment_id"] = comments_data[
                    "last_comment_id"
                ]
                self.s3.Object(key=key).put(Body=item_to_yml(source_data))
        except Exception as e:
            log.exception(e)
        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            self.s3 = boto3.resource("s3").Bucket(S3_BUCKET)
            log.info(
                f"Data will be stored to the S3 bucket {S3_BUCKET} Root key: reddit.com",
            )


class S3ModelSP500Pipeline(S3Pipeline, PipelineSettingsMixin):
    """Store Companies Model data to the S3 bucket."""

    s3 = None
    SETTINGS_KEY = "TO_S3"
    data_dir = "model_data/"
    file_prefix = "data_file_"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        try:
            if self.s3:
                current_datetime = datetime.datetime.now()
                key = f"{self.data_dir}{self.file_prefix}{current_datetime.isoformat()}.json"
                self.s3.Object(key=key).put(Body=json.dumps(item["data"]))
        except Exception:
            log.exception("Unexpected error")
        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            if spider.s3_dir_key:
                self.data_dir = spider.s3_dir_key
            if spider.file_prefix:
                self.file_prefix = spider.file_prefix
            self.s3 = boto3.resource("s3").Bucket(S3_BUCKET)
            log.info(
                f"Data will be stored to the S3 bucket {S3_BUCKET} Root key: {self.data_dir}",
            )


class S3ModelCalendarsPipeline(S3Pipeline, PipelineSettingsMixin):
    """Store Companies Model data to the S3 bucket."""

    s3 = None
    SETTINGS_KEY = "TO_S3"
    data_dir = "calendar_data/"
    file_prefix = "calendar_file_"

    def __init__(self) -> None:
        """Initialize pandas data frame."""
        self.frame = []

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """Process scraped item based on conditions."""
        item_data = json.loads(item.get("data")[0])
        if item_data:
            self.frame.append(item_data)
        return item

    def close_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is closed."""
        try:
            if self.s3:
                d = json.dumps(self.frame).encode("utf-8")
                data = io.BytesIO(d)
                current_datetime = datetime.datetime.now()
                key = f"{self.data_dir}{self.file_prefix}{current_datetime.isoformat()}.json"
                conf = TransferConfig(multipart_threshold=62500, max_concurrency=4)
                self.s3.Object(key=key).upload_fileobj(data, Config=conf)
        except Exception:
            log.exception("Unexpected error")
        log.info(f"Spider {spider.name} closed")

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            if spider.s3_dir_key:
                self.data_dir = spider.s3_dir_key
            if spider.file_prefix:
                self.file_prefix = spider.file_prefix
            self.s3 = boto3.resource("s3").Bucket(S3_BUCKET)
            log.info(
                f"Data will be stored to the S3 bucket {S3_BUCKET} Root key: {self.data_dir}",
            )


class S3JsonPipeline(S3Pipeline, PipelineSettingsMixin):
    """Store json files from dataframe to the S3 bucket."""

    s3 = None
    SETTINGS_KEY = "TO_S3"
    data_dir = "companies-models-data"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """Process scraped item based on conditions."""
        try:
            if self.s3:
                d = (
                    item.get("data")[0].encode("utf-8")
                    if spider.name != "global_data"
                    else item["data"].encode("utf-8")
                )
                data = io.BytesIO(d)
                current_datetime = datetime.datetime.now()
                path = f"{self.data_dir}/{spider.s3_dir_key}/{spider.file_prefix}"
                key = f"{path}_{current_datetime.isoformat()}.json"
                conf = TransferConfig(multipart_threshold=62500, max_concurrency=4)
                self.s3.Object(key=key).upload_fileobj(data, Config=conf)
        except Exception:
            log.exception("Unexpected error")
        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            self.s3 = boto3.resource("s3").Bucket(S3_BUCKET)
            log.info(
                f"Data will be stored to the S3 bucket {S3_BUCKET} Root key: {self.data_dir}",
            )


class S3CSVPipeline(S3Pipeline):
    """Write CSV file from buffer to S3 as a gzip."""

    s3 = None
    SETTINGS_KEY = "TO_S3"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """Will be called for each scraped item."""
        if strtobool(self.active):
            try:
                row = ItemAdapter(item).asdict()
                self.writer.writerow(row)
            except Exception:
                log.exception("Unexpected error")
            return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """Will be called on spider start."""
        if strtobool(self.active):
            super(S3CSVPipeline, self).open_spider(spider)
            self.csvbuff = io.StringIO()
            self.writer = csv.DictWriter(
                self.csvbuff, fieldnames=spider.__getattribute__("csv_fieldnames")
            )
            self.writer.writeheader()

    def close_spider(self, spider: scrapy.Spider) -> None:
        """Make gzip file with scraped data on spider close."""
        if strtobool(self.active):
            s_out = gzip.compress(self.csvbuff.getvalue().encode())
            data = io.BytesIO(s_out)
            key = f"{spider.name}/{spider.__getattribute__('csv_filename')}.csv.gz"
            conf = TransferConfig(multipart_threshold=62500, max_concurrency=4)
            self.s3.Object(key=key).upload_fileobj(data, Config=conf)


class S3CSVDailyAggPipeline(S3Pipeline):
    """Write CSV file from buffer to S3 as a gzip."""

    s3 = None
    SETTINGS_KEY = "TO_S3"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """Process scraped items and make gzip file for each ticker."""
        if strtobool(self.active):
            csvbuff = io.StringIO()
            writer = csv.DictWriter(csvbuff, fieldnames=spider.__getattribute__("csv_fieldnames"))
            writer.writeheader()
            try:
                data = ItemAdapter(item).asdict()
                for row in data["result"]:
                    row["ticker"] = item.get("ticker")
                    writer.writerow(row)
                s_out = gzip.compress(csvbuff.getvalue().encode())
                data = io.BytesIO(s_out)
                key = f"{spider.name}/{item.get('ticker')}_{spider.__getattribute__('csv_filename')}.csv.gz"
                conf = TransferConfig(multipart_threshold=62500, max_concurrency=4)
                self.s3.Object(key=key).upload_fileobj(data, Config=conf)
            except Exception:
                log.exception("Unexpected error")
            return item


class FredMacroS3Pipeline(S3Pipeline, PipelineSettingsMixin):
    """Pipeline for fin_calendars spider."""

    s3 = None
    path: Optional[Path] = None
    SETTINGS_KEY = "TO_S3"

    def __init__(self) -> None:
        """Initialize pandas data frame."""
        self.frame = {}
        self.k = 0

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """Process scraped item based on conditions."""
        data = json.loads(item["data"])
        macro = item["ticker"]
        self.frame.update({macro: data})
        return item

    def close_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is closed."""
        try:
            if self.s3:
                encoded = json.dumps(self.frame).encode("utf-8")
                data = io.BytesIO(encoded)
                current_datetime = datetime.datetime.now()
                key = f"{self.data_dir}{self.file_prefix}{current_datetime.isoformat()}.json"
                conf = TransferConfig(multipart_threshold=62500, max_concurrency=4)
                self.s3.Object(key=key).upload_fileobj(data, Config=conf)
        except Exception:
            log.exception("Unexpected error")
        log.info(f"Spider {spider.name} closed")

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            if spider.__getattribute__("s3_dir_key"):
                self.data_dir = spider.__getattribute__("s3_dir_key")
            if spider.__getattribute__("file_prefix"):
                self.file_prefix = spider.__getattribute__("file_prefix")
            self.s3 = boto3.resource("s3").Bucket(S3_BUCKET)
            log.info(
                f"Data will be stored to the S3 bucket {S3_BUCKET} Root key: {self.data_dir}",
            )


class S3IntrinioDataPipeline(S3Pipeline, PipelineSettingsMixin):
    """Store Companies Model data items to the local file system."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_S3"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        data = item.get("data")
        ticker = item.get("ticker")
        try:
            if self.s3:
                encoded = json.dumps(data).encode("utf-8")
                b = io.BytesIO(encoded)
                current_datetime = datetime.datetime.now()
                key = f"{self.data_dir}{ticker}/{ticker}_{current_datetime.isoformat()}.json"
                conf = TransferConfig(multipart_threshold=62500, max_concurrency=4)
                self.s3.Object(key=key).upload_fileobj(b, Config=conf)
                log.info("Data for %s were sent to S3 bucket" % item.get("ticker"))
        except Exception:
            log.exception("Unexpected error")

        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        super(S3IntrinioDataPipeline, self).open_spider(spider)
        # self.frame = {}
        if strtobool(self.active):
            if spider.__getattribute__("s3_dir_key"):
                self.data_dir = spider.__getattribute__("s3_dir_key")
            if spider.__getattribute__("file_prefix"):
                self.file_prefix = spider.__getattribute__("file_prefix")


class S3DataPipeline(S3Pipeline, PipelineSettingsMixin):
    """Store Companies Model data items to the local file system."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_S3"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        data = item.get("data")
        try:
            if self.s3:
                current_datetime = datetime.datetime.now()
                extension = "csv" if spider.name == "intrinio_quarter" else "xls"
                key = (
                    f"{spider.__getattribute__('s3_dir_key')}{spider.__getattribute__('file_prefix')}"
                    f"{current_datetime.isoformat().replace(':', '_')}.{extension}.gz"
                )
                if spider.name != "intrinio_quarter":
                    str_out = gzip.compress(data)
                    data = io.BytesIO(str_out)
                conf = TransferConfig(multipart_threshold=62500, max_concurrency=4)
                self.s3.Object(key=key).upload_fileobj(data, Config=conf)
        except Exception:
            log.exception("Unexpected error")
        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            self.s3 = boto3.resource("s3").Bucket(S3_BUCKET)
            log.info(
                f"Data will be stored to the S3 bucket {S3_BUCKET}",
            )

    def close_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is closed."""
        log.info(f"Spider {spider.name} closed")


class S3MultipartPipeline(S3Pipeline, PipelineSettingsMixin):
    """Store Companies Model data items to the local file system."""

    s3_client = None
    s3_resource = None
    path: Optional[Path] = None
    SETTINGS_KEY = "TO_S3"
    part_threshold = 1024 * 1024 * 50

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        url = item.get("url")
        source = item.get("source")
        key = item.get("s3_key")
        try:
            if self.s3:
                multipart_upload = self.s3_client.create_multipart_upload(
                    Bucket=self.s3.name,
                    Key=key,
                )
                with http.get(url, stream=True) as r:
                    r.raise_for_status()
                    num = 1
                    parts = []
                    if int(r.headers.get("content-length")) >= self.part_threshold:
                        log.info(f"Started multipart uploading: {source}")
                        for chunk in r.iter_content(self.part_threshold):
                            upload_part = self.s3_resource.MultipartUploadPart(
                                self.s3.name, key, multipart_upload["UploadId"], num
                            )
                            upload_part_response = upload_part.upload(
                                Body=chunk,
                            )
                            parts.append({"PartNumber": num, "ETag": upload_part_response["ETag"]})
                            log.info("Created meta for chunk %d", num)
                            num += 1
                        self.s3_client.complete_multipart_upload(
                            Bucket=self.s3.name,
                            Key=key,
                            MultipartUpload={"Parts": parts},
                            UploadId=multipart_upload["UploadId"],
                        )
                        log.info(f"Completed multipart uploading: {source}")
                    else:
                        log.info(f"Started simple uploading: {source}")
                        self.s3.Object(key=key).upload_fileobj(r.raw)
                        log.info(f"Completed simple uploading: {source}")
        except Exception:
            log.exception("Unexpected error")
        return item

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            self.s3_client = boto3.client("s3")
            self.s3_resource = boto3.resource("s3")
            self.s3 = self.s3_resource.Bucket(S3_BUCKET)
            log.info(
                f"Data will be stored to the S3 bucket {S3_BUCKET}",
            )

    def close_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is closed."""
        log.info(f"Spider {spider.name} closed")


class BaseAPIPipeline(object):
    """Base class for non-blocking API pipelines."""

    active = False
    SETTINGS_KEY: Optional[str] = None
    api = None
    concurrency = 8
    delay = 0
    slot = "base"
    login = None
    name = None
    password = None

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if strtobool(self.active):
            slot = Slot(concurrency=self.concurrency, delay=self.delay, randomize_delay=True)
            spider.crawler.engine.downloader.slots[self.slot] = slot
            log.info(f"{self.name} - {self.api}")
            log.debug(f"{self.login} {self.password}")

    async def request(
        self, payload: dict, spider: scrapy.Spider, method: str = "POST", status: int = 200
    ) -> Any:
        """Scrapy request handler."""
        request = scrapy.Request(
            self.api,
            method=method,
            body=json.dumps(payload),
            headers=build_headers(self.login, self.password),
            meta={"download_slot": self.slot},
        )
        r = await spider.crawler.engine.download(request, spider)
        if r.status != status:
            log.warning(f"{r.url} {r.json()}")
            raise ValueError(f"{r.url} {r.json()}")
        if r.text:
            return r.json()

    async def update_item(self, item: scrapy.Item, spider: scrapy.Spider) -> None:
        """Must be implemented in the inherited classes."""
        raise NotImplementedError

    async def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        if strtobool(self.active):
            ts = arrow.now()
            try:
                await self.update_item(item, spider)
            except Exception:
                log.exception(f"{self.name} pipeline error. " f"Execution time: {arrow.now() - ts}")
                log.debug(f"Item text: {item.get('text')}")
            else:
                log.debug(
                    f'{self.name} {item.get("url")} done. '
                    f'Text size: {len(item.get("text", ""))} Execution time: {arrow.now() - ts}'
                )
        return item


class TopicClassificationPipeline(BaseAPIPipeline, PipelineSettingsMixin):
    """Item topic tags update."""

    SETTINGS_KEY = "TOPIC_CLASSIFICATION"
    api = f"{MODELS_API_URL}/categorization"
    slot = "topic"
    login = MODELS_API_USER
    name = "Topic classification"
    password = MODELS_API_PASSWORD

    async def update_item(self, item: scrapy.Item, spider: scrapy.Spider) -> None:
        """Update item tags."""
        payload = dict(text=item["text"])
        topic_tags = await self.request(payload, spider)
        item["tags"] = spider.tags + topic_tags

    @classmethod
    def from_crawler(cls, crawler: Any) -> "TopicClassificationPipeline":
        """This is the class method used by Scrapy to create pipeline class instance."""
        cls.set_settings_val(crawler)
        return cls()


class SentimentClassificationPipeline(BaseAPIPipeline, PipelineSettingsMixin):
    """Items topic sentiment classification."""

    SETTINGS_KEY = "SENTIMENT_CLASSIFICATION"
    api = f"{MODELS_API_URL}/sentiments"
    slot = "sentiments"
    login = MODELS_API_USER
    name = "Sentiment classification"
    password = MODELS_API_PASSWORD

    async def update_item(self, item: scrapy.Item, spider: scrapy.Spider) -> None:
        """Update spider item."""
        topic_tags = [e for e in item["tags"] if e not in spider.tags]
        if topic_tags:
            payload = dict(text=item["text"], topics=topic_tags)
            item["sentiment"] = await self.request(payload, spider)
        else:
            item["sentiment"] = {}

    @classmethod
    def from_crawler(cls, crawler: Any) -> "SentimentClassificationPipeline":
        """This is the class method used by Scrapy to create pipeline class instance."""
        cls.set_settings_val(crawler)
        return cls()


class APIPipeline(BaseAPIPipeline, PipelineSettingsMixin):
    """Store items to AI API."""

    SETTINGS_KEY = "TO_API"
    api = None
    slot = "datalake"
    login = DATALAKE_API_USER
    name = "Datalake"
    password = DATALAKE_API_PASSWORD
    stats = None

    def __init__(self, stats: scrapy.statscollectors.MemoryStatsCollector) -> None:
        """Connect crawler stats to pipeline."""
        self.stats = stats

    def open_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is opened."""
        if spider.name == "yahoo-finance":
            self.api = f"{DATALAKE_API_URL}/stocks/prices"
        else:
            self.api = f"{DATALAKE_API_URL}/texts"
        super(APIPipeline, self).open_spider(spider)

    async def text_to_payload(self, item: scrapy.Item) -> dict:
        """Convert ArticleItem to request payload."""
        payload = dict(
            author=item.get("author"),
            created_at=item["created_at"],
            src=item["src"],
            tags=item["tags"],
            text=item["text"],
            title=item.get("title", ""),
            url=item["url"],
            meta=item.get("meta", {}),
        )
        if item.get("sentiment") is not None:
            payload["sentiment"] = item["sentiment"]
        return payload

    async def ticker_to_payload(self, item: scrapy.Item) -> dict:
        """Convert TickerItem to request payload."""
        data_keys = ["close", "dividends", "high", "low", "open", "splits", "volume"]
        payload = dict(
            ticker=item["ticker"],
            date=item["date"],
            data={k: item[k] for k in item.keys() if k in data_keys},
        )
        return payload

    async def update_item(self, item: scrapy.Item, spider: scrapy.Spider) -> None:
        """Add text to the datalake."""
        converters = {
            TickerItem: self.ticker_to_payload,
            ArticleItem: self.text_to_payload,
            EquityArticleItem: self.text_to_payload,
            TweetItem: self.text_to_payload,
            RedditSubredditItem: self.text_to_payload,
            RedditSearchItem: self.text_to_payload,
            AudioEpisodeItem: self.text_to_payload,
            GoogleTrendsItem: self.text_to_payload,
            YoutubeVideoItem: self.text_to_payload,
        }
        payload = await converters[type(item)](item)

        try:
            await self.request(payload, spider, status=201)
        except ValueError:
            return

    def close_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is closed."""
        log.info(f"Spider {spider.name} closed")
        stats = self.stats.get_stats()
        items = stats.get("item_scraped_count", 0)
        errors = stats.get("log_count/ERROR", 0)
        article_errors = stats.get("spidermon/validation/items/errors", 0)
        log.info({"items": items, "errors": errors, "article_errors": article_errors})
        if errors:
            payload = {"status": "failed"}
        else:
            payload = {"status": "active"}
        if spider.name not in ["twitter", "reddit.com"] and strtobool(self.active):
            update_status(payload, spider.name)

    @classmethod
    def from_crawler(cls, crawler: Any) -> "APIPipeline":
        """This is the class method used by Scrapy to create pipeline class instance."""
        cls.set_settings_val(crawler)
        return cls(crawler.stats)


class APICommentsPipeline(APIPipeline):
    """API pipeline uses for updating comments for text."""

    async def text_to_payload(self, item: scrapy.Item) -> dict:
        """Convert RedditCommentsItem to request payload."""
        payload = dict(
            id=item.get("text_id")[0],
            comments_text=f"\n{item.get('comments_text')}",
            url=item.get("url"),
            last_comment_id=item.get("last_comment_id")[0],
        )
        return payload

    async def update_item(self, item: scrapy.Item, spider: scrapy.Spider) -> None:
        """Add text to the datalake."""
        converters = {RedditCommentsItem: self.text_to_payload}

        payload = await converters[type(item)](item)

        try:
            await self.request(payload, spider, status=204)
        except ValueError:
            return

    async def request(
        self, payload: dict, spider: scrapy.Spider, method: str = "PUT", status: int = 204
    ) -> Any:
        """Scrapy request handler."""
        request = scrapy.Request(
            self.api + f"/{payload.get('id')}",
            method=method,
            body=json.dumps(payload),
            headers=build_headers(self.login, self.password),
            meta={"download_slot": self.slot},
        )
        r = await spider.crawler.engine.download(request, spider)
        if r.status != status:
            log.warning(f"{r.url} {r.json()}")
            raise ValueError(f"{r.url} {r.json()}")
        if r.text:
            return r.json()


class APIPipelineReport(APIPipeline):
    """This pipeline sends stats data to an appropriate data source.

    It doesn't send any items to Data Lake DB, only reporting about spider status.
    """

    async def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        if strtobool(self.active):
            ts = arrow.now()
            log.debug(
                f'{self.name} {item.get("url")} done. '
                f'Text size: {len(item.get("text", ""))} Execution time: {arrow.now() - ts}'
            )
        return item


class NotifierPipeline(PipelineSettingsMixin):
    """Send report to Slack."""

    SETTINGS_KEY = "TO_SLACK"
    stats = None
    notifier = None
    processed = 0
    persons = [SPIDER_AUTHORS_SLACK_IDS[YURI]]
    name = "Notifier"

    def __init__(self, stats: scrapy.statscollectors.MemoryStatsCollector) -> None:
        """Connect crawler stats to pipeline."""
        self.stats = stats
        if strtobool(self.active):
            self.notifier = boto3.client("lambda")

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """This method is called for every item pipeline component."""
        self.processed += 1
        return item

    def close_spider(self, spider: scrapy.Spider) -> None:
        """This method is called when the spider is closed."""
        if spider.name == "twitter" or not strtobool(self.active):
            return
        try:
            stats = self.stats.get_stats()
            scraped = stats.get("item_scraped_count", 0)
            errors = stats.get("log_count/ERROR", 0)
            article_errors = stats.get("spidermon/validation/items/errors", 0)
            msg = (
                f"Scraped: {scraped}, processed: {self.processed}, "
                f"errors: {errors}, article errors: {article_errors}"
            )
            if spider.cloud_watch_log_url:
                msg += f" Cloudwatch log {spider.cloud_watch_log_url}"
            if spider.get_spider_author() not in self.persons:
                self.persons.append(spider.get_spider_author())
            payload = {
                "msg": msg,
                "msg_type": "error" if errors else "info",
                "src": f"Scrapy spider {spider.name}, environment {ENVIRONMENT}",
                "cc": self.persons if errors else [],
            }
            response = self.notifier.invoke(
                FunctionName=NOTIFIER_ARN, Payload=json.dumps(payload).encode()
            )
            if response["StatusCode"] != 200:
                raise ValueError("Notifier error")
        except Exception:
            log.exception(f"{self.name} pipeline error")

    @classmethod
    def from_crawler(cls, crawler: Any) -> "NotifierPipeline":
        """This is the class method used by Scrapy to create pipeline class instance."""
        cls.set_settings_val(crawler)
        return cls(crawler.stats)


class LanguageDetectionPipeline:
    """Drop all the items having text not in English."""

    @staticmethod
    def process_item(item: scrapy.Item, spider: scrapy.Spider) -> Any:
        """This method is called for every item pipeline component."""
        try:
            language = detect(item["text"])
        except LangDetectException as e:
            raise DropItem("Dropping the item: %s" % e)
        else:
            if language == "en":
                return item
            else:
                raise DropItem("Dropping the item with url: %s" % item["url"])


class FSJsonPipeline(FSPipeline, PipelineSettingsMixin):
    """Pipeline for storing Json file from Data frame."""

    path: Optional[Path] = None
    SETTINGS_KEY = "TO_FILE"

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        """Process scraped item based on conditions."""
        try:
            if self.path and strtobool(self.active):
                current_datetime = datetime.datetime.now()
                name = self.path / f"{spider.file_prefix}_{current_datetime.isoformat()}.json"
                with name.open("w", encoding="utf-8") as f:
                    f.write(item["data"][0] if spider.name != "global_data" else item["data"])
        except Exception:
            log.exception("Unexpected error")
        return item
