"""Scrapy settings for agblox project.

For simplicity, this file contains only settings considered important or
commonly used.

References:
    https://docs.scrapy.org/en/latest/topics/settings.html
"""
from distutils.util import strtobool
import os
from pathlib import Path

from agblox.items import ArticleItem, EquityArticleItem, RedditSearchItem, RedditSubredditItem
from dotenv import load_dotenv


env_file = Path(__file__).parent.absolute().parent.parent / ".env"
load_dotenv(dotenv_path=env_file, verbose=True)

BOT_NAME = "agblox"

SPIDER_MODULES = ["agblox.spiders"]
NEWSPIDER_MODULE = "agblox.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT_SELENIUM = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/87.0.4280.88 Safari/537.36 "
)

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'agblox.middlewares.AgbloxSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "agblox.middlewares.RotatingProxyDownloaderMiddleware": None,
    "rotating_proxies.middlewares.BanDetectionMiddleware": None,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
}

ROTATING_PROXY_BAN_POLICY = "agblox.policy.AgBloxBanPolicy"

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
CONCURRENT_ITEMS = 1000
ITEM_PIPELINES = {
    "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 300,
    "agblox.pipelines.FSPipeline": 310,
    "agblox.pipelines.S3Pipeline": 320,
    "agblox.pipelines.TopicClassificationPipeline": 330,
    # "agblox.pipelines.SentimentClassificationPipeline": 340,
    "agblox.pipelines.APIPipeline": 350,
    "agblox.pipelines.NotifierPipeline": 500,
}

SPIDERMON_VALIDATION_MODELS = {
    ArticleItem: "agblox.items.ArticleValidateItem",
    EquityArticleItem: "agblox.items.EquityArticleValidateItem",
    RedditSubredditItem: "agblox.items.RedditSubredditValidateItem",
    RedditSearchItem: "agblox.items.RedditSearchValidateItem",
}

SPIDERMON_ENABLED = True
SPIDERMON_VALIDATION_DROP_ITEMS_WITH_ERRORS = True
SPIDERMON_VALIDATION_ADD_ERRORS_TO_ITEMS = True

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

SELENIUM_DRIVER_NAME = "chrome"
SELENIUM_COMMAND_EXECUTOR = os.getenv("SELENIUM_COMMAND_EXECUTOR", "http://127.0.0.1:4444/wd/hub")
SELENIUM_DRIVER_ARGUMENTS = ["--headless", f"user-agent={USER_AGENT_SELENIUM}"]

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

TO_FILE = os.getenv("TO_FILE", None)
KEEP_VIDEO = os.getenv("KEEP_VIDEO", None)

TO_S3 = os.getenv("TO_S3", None)
S3_BUCKET = os.getenv("S3_BUCKET", None)

TO_API = os.getenv("TO_API", None)
DATALAKE_API_URL = os.getenv("API_URL", "https://demo.datalake.diviai.com/")
DATALAKE_API_USER = os.getenv("API_USER", None)
DATALAKE_API_PASSWORD = os.getenv("API_PASSWORD", None)

API_LOG_409 = strtobool(os.getenv("API_LOG_409", "1"))  # Log 409 API errors as warning if False

TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", None)
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", None)
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY", None)
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET", None)

GHUB_ACCESS_TOKEN = os.getenv("GHUB_ACCESS_TOKEN", None)

MODELS_API_URL = os.getenv("MODELS_API_URL", "http://127.0.0.1:5050")
MODELS_API_USER = os.getenv("MODELS_API_USER", None)
MODELS_API_PASSWORD = os.getenv("MODELS_API_PASSWORD", None)

TOPIC_CLASSIFICATION = os.getenv("TOPIC_CLASSIFICATION", None)
SENTIMENT_CLASSIFICATION = os.getenv("SENTIMENT_CLASSIFICATION", None)

TO_SLACK = os.getenv("TO_SLACK", None)
NOTIFIER_ARN = os.getenv("NOTIFIER_ARN")
ECS_CONTAINER_METADATA_URI = os.getenv("ECS_CONTAINER_METADATA_URI")

ENVIRONMENT = os.getenv("ENVIRONMENT")

TO_CLOUDWATCH = strtobool(os.getenv("TO_CLOUDWATCH", "0"))
AWS_REGION = os.getenv("AWS_DEFAULT_REGION")

REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")

LINKEDIN_EMAIL = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

FINANCIAL_MODELING_PREP_API_KEY = os.getenv("FINANCIAL_MODELING_PREP_API_KEY", None)
FRED_API_KEY = os.getenv("FRED_API_KEY", None)

PROXY_ENABLED = os.getenv("PROXY_ENABLED", None)

INTRINIO_API_KEY = os.getenv("INTRINIO_API_KEY", None)

POLYGON_ACCESS_TOKEN = os.getenv("POLYGON_ACCESS_TOKEN", None)

CLOSESPIDER_ERRORCOUNT = 20

ARKADY = "Arkady Bagdasarov"
CLAUDIO = "Claudio Lichtenthal"
DANIEL = "Daniel Moore"
DANIYAL = "Daniyal Tariq"
EZEQUIEL = "Ezequiel Salas"
YURI = "Yuri Grytsai"
IAROSLAV = "iaro"
JOSHUA = "Joshua Yoder"
BORIS = "Boris Litvyakov"
ROSS = "Ross Botticelli"
AZKA = "Azka Minhas"

SPIDER_AUTHORS_SLACK_IDS = {
    ARKADY: "U01F569R6F7",
    AZKA: "U02BR1WCT4H",
    CLAUDIO: "U0298LRSWV9",
    DANIEL: "U012K3DFV6D",
    DANIYAL: "U02B4MF3DF0",
    EZEQUIEL: "U01BBMTUUN5",
    YURI: "U01LA0ZP14Z",
    IAROSLAV: "UJX8UR5J5",
    JOSHUA: "U013YF3DJVC",
    BORIS: "U01TP2XV941",
    ROSS: "U024HBHJPPC",
}
