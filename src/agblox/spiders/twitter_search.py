"""Spider that interacts with Twitter Search API and looks for the data related to the given tickers."""
import json
import logging
from typing import Dict, Iterator

from agblox.items import TweetItem
from agblox.settings import (
    BORIS,
    DATALAKE_API_PASSWORD,
    DATALAKE_API_URL,
    DATALAKE_API_USER,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
)
from agblox.spiders.helpers import EquitySpider
import arrow
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.util.retry import Retry
import scrapy
from scrapy.http import TextResponse
import tweepy

log = logging.getLogger(__name__)
session = requests.session()
retry = Retry(connect=5, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)


class TwitterSearch(EquitySpider):
    """Spider that sends queries to the twitter Search API and saves tweets returned."""

    name: str = "twitter_search"
    host_header = "twitter.com"
    tweets_per_query: int = 100
    api: tweepy.API = None
    spider_author = BORIS

    def init_api(self) -> None:
        """Connect to twitter."""
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def get_from_status(self, status: tweepy.Status) -> Dict:
        """Collects metadata from Status object if tweet is a retweet."""
        return {
            "author": f"@{status.author.screen_name}".lower(),
        }

    def get_max_id(self, ticker: str) -> int:
        """Return maximal id of a tweet related to a given ticker that is stored at the datalake."""
        if not DATALAKE_API_URL:
            raise Exception("No API URL provided.")

        payload = {
            "limit": 100,
            "sort_order": "desc",
            "tags": ["twitter", "equity", ticker],
            "with_sentiment": False,
            "with_count": False,
        }

        r = session.get(
            f"{DATALAKE_API_URL}/texts",
            params=payload,
            auth=HTTPBasicAuth(DATALAKE_API_USER, DATALAKE_API_PASSWORD),
        )  # TODO Redo it to behave like all spiders config
        if r.status_code != 200:
            log.error(r.text)

        tweets = json.loads(r.text)
        return (
            max(
                tweet["meta"]["tweet_data"]["id"]
                for tweet in tweets
                if tweet["meta"].get("tweet_data")
            )
            if tweets
            else 0
        )

    def page_to_items(self, page: tweepy.models.SearchResults, ticker: str) -> Iterator[TweetItem]:
        """Gets tweepy search page as input and yields TweetItem objects."""
        for tweet in page:
            item = TweetItem()
            author = f"@{tweet.author.screen_name}".lower()
            item["meta"] = {}
            item["meta"]["tweet_data"] = {}
            item["author"] = author
            item["created_at"] = arrow.get(tweet.created_at).for_json()
            item["raw"] = tweet._json
            item["tags"] = self.tags + ["twitter", author, ticker]

            try:  # https://stackoverflow.com/a/55119585/4249707
                item["text"] = tweet.retweeted_status.full_text
                item["meta"]["tweet_data"]["retweeted_status"] = self.get_from_status(
                    tweet.retweeted_status
                )
            except AttributeError:
                item["text"] = tweet.full_text
            item["title"] = ""
            item["url"] = f"https://twitter.com/{tweet.author.id}/status/{tweet.id}"
            item["meta"]["base_ticker"] = ticker
            item["meta"]["tweet_data"][
                "profile_image_url_https"
            ] = tweet.author.profile_image_url_https
            item["meta"]["tweet_data"]["id"] = tweet.id
            item["meta"]["tweet_data"]["favorite_count"] = tweet.favorite_count
            item["meta"]["tweet_data"]["retweet_count"] = tweet.retweet_count
            item["meta"]["tweet_data"]["author_id"] = tweet.author.id
            item["meta"]["tweet_data"]["author_followers_count"] = tweet.author.followers_count
            item["meta"]["tweet_data"]["author_friends_count"] = tweet.author.friends_count
            item["meta"]["tweet_data"]["author_favourites_count"] = tweet.author.favourites_count
            item["meta"]["tweet_data"]["in_reply_to_screen_name"] = tweet.in_reply_to_screen_name
            item["meta"]["tweet_data"]["in_reply_to_user_id"] = tweet.in_reply_to_user_id
            item["meta"]["tweet_data"]["retweeted"] = tweet.retweeted
            item["meta"]["tweet_data"]["entities"] = tweet.entities
            item["meta"]["tweet_data"]["lang"] = tweet.lang
            item["meta"]["tweet_data"]["user_listed_count"] = tweet.user.listed_count

            yield item

    def start_requests(self) -> Iterator[scrapy.Request]:
        """Placeholder that overrides EquitySpider function."""
        yield scrapy.Request("https://twitter.com/", callback=self.parse)

    def parse(self, response: TextResponse) -> Iterator[TweetItem]:
        """Parsing tweets."""
        self.init_api()

        tickers = self.get_tickers_from_api(limit=6000, sort_order="volume")

        for ticker in tickers:
            max_id = self.get_max_id(ticker["ticker"])
            log.info(f"Starting to process ticker {ticker['ticker']} | max_id {max_id}")

            try:
                for page in tweepy.Cursor(
                    self.api.search,
                    q=f"${ticker['ticker']}",
                    count=100,
                    since_id=max_id,
                    lang="en",
                    tweet_mode="extended",
                ).pages(10):
                    for item in self.page_to_items(page, ticker["ticker"]):
                        yield item
            except tweepy.error.TweepError as e:
                log.info(f"There is an error in Tweepy module: {e}")
                continue
