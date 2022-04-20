"""Spider middlewares.

References:
    https://docs.scrapy.org/en/latest/topics/spider-middleware.html
"""

# flake8: noqa
# Auto generated examples. Must be removed for real code.
import requests
from timeit import default_timer as timer
from typing import Any
from urllib.parse import urlencode, urlparse
from w3lib.http import basic_auth_header

import feedparser
from rotating_proxies.middlewares import RotatingProxyMiddleware
from scrapy import signals
from scrapy.exceptions import CloseSpider
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from agblox.settings import PROXY_ENABLED, MODELS_API_URL, DATALAKE_API_URL


class MiddlewaresSettingsMixin:
    """Mixin for middleware configuration based on settings status after crawler was created."""

    SETTINGS_KEY: str = None
    active = None

    @classmethod
    def set_settings_val(cls, crawler):
        """This is the class method used by this mixin to reassign settings values"""
        cls.active = crawler.settings[cls.SETTINGS_KEY]


class AgbloxSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AgbloxDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class RotatingProxyDownloaderMiddleware(RotatingProxyMiddleware, MiddlewaresSettingsMixin):
    """Override middleware with proxies support."""

    SETTINGS_KEY = "PROXY_ENABLED"

    @classmethod
    def from_crawler(cls, crawler):
        cls.set_settings_val(crawler)
        if not cls.active:
            return crawler

        settings = crawler.settings.copy()
        settings.frozen = False
        settings.setdict({"ROTATING_PROXY_LIST": crawler.cfg.get("proxies", [])})
        settings.freeze()
        crawler.settings = settings
        return super(RotatingProxyDownloaderMiddleware, cls).from_crawler(crawler)

    def process_request(self, request, spider):
        #  skip proxy for our infrastructure
        if MODELS_API_URL in request.url or DATALAKE_API_URL in request.url:
            return
        super().process_request(request, spider)


class RedditDownloaderMiddleware:
    """Consists of methods for handling auth flow for Reddit API."""

    token_expires_in = 3600  # token will be refreshed after that pepriod -50 sec by default

    @classmethod
    def from_crawler(cls, crawler):
        """Uses signal for connect to the spider."""
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """Checks particular request for auth token existance."""
        if urlparse(request.url).hostname in ["oauth.reddit.com", "www.reddit.com"]:

            auth = getattr(self, "auth", None)
            if auth and b"Authorization" not in request.headers:
                request.headers[b"Authorization"] = auth

            access_token = getattr(self, "access_token", None)
            if access_token:
                if timer() - self.start <= self.token_expires_in - 50:
                    request.headers[b"Authorization"] = f"bearer {access_token}"
                else:
                    self.refresh_token(request)
                    spider.logger.info("TOKEN was updated.")
            return None

    def process_response(self, request, response, spider):
        """Processes response from reddit.com only for handle auth flow and refreshing the token."""
        if urlparse(request.url).hostname in ["oauth.reddit.com", "www.reddit.com"]:
            access_token = getattr(self, "access_token", None)  # check if we have token already
            if not access_token:
                self.update_token(response)
                spider.logger.info("TOKEN was received.")

        return response

    def spider_opened(self, spider):
        """Sets basic auth parameters during opening the spider."""
        spider.logger.info("Spider opened: %s" % spider.name)
        self.usr = getattr(spider, "http_user", "")
        self.pwd = getattr(spider, "http_pass", "")
        client_id = getattr(spider, "client_id", "")
        client_secret = getattr(spider, "client_secret", "")
        self.auth_payload = {
            "grant_type": "password",
            "username": self.usr,
            "password": self.pwd,
        }
        if client_id or client_secret:
            self.auth = basic_auth_header(client_id, client_secret)

    def update_token(self, response) -> None:
        """Updates token from received response."""
        r = response.json()
        self.start = timer()
        try:
            self.access_token = r["access_token"]
            self.token_expires_in = r["expires_in"]
        except Exception as e:
            raise CloseSpider(f"Some Exception was ossured while token update.")

    def refresh_token(self, request):
        """Provides the new token for futher use."""
        headers = {
            "User-Agent": "DiviAIApp/0.1.0 by /u/yugritsai email: yugritsai@gmail.com",
            "Authorization": self.auth,
        }

        r = requests.post(
            url="https://www.reddit.com/api/v1/access_token",
            data=self.auth_payload,
            headers=headers,
        )
        self.update_token(r)

        return None


class GTRetryMiddleware(RetryMiddleware):
    """Middleware for checking data from Google Trends."""

    def process_response(self, request, response, spider):
        if request.meta.get("dont_retry", False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        # Check if Google Trends items are not empty
        if response.status == 200:
            d = feedparser.parse(response.text)
            try:
                items = d["items"]
            except KeyError:
                items = []
            if not items:
                return self._retry(request, "Empty Google Trends items", spider) or response
        return response
