"""Tweets collection spider."""
import logging
from typing import Dict, Iterator, Optional, Tuple

from agblox.items import TweetItem
from agblox.settings import (
    ARKADY,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
)
from agblox.spiders.helpers import BaseSpider, update_status
import arrow
import scrapy
from scrapy.http import TextResponse
import tweepy

log = logging.getLogger(__name__)


class NoMoreTweets(Exception):
    """No more tweets to scrape exception."""

    pass


class TwitterSpider(BaseSpider):
    """Spider for tweets."""

    name: str = "twitter"
    host_header = "twitter.com"
    tweets_per_query: int = 250
    max_tweets: int = 3500  # tweets total
    api: tweepy.API = None
    spider_author = ARKADY

    def twitter_users(self) -> Iterator[Tuple[str, dict]]:
        """Get twitter users."""
        users = self.get_cfg()
        for user, cfg in users.items():
            status = cfg.pop("status")
            if status in ["stopped", "deleted"]:
                log.info(f"User {user} skipped by status. Status: {status}")
            else:
                if "tweet" not in cfg["tags"]:
                    cfg["tags"].append("tweet")
                if "Stocks" in cfg["tags"]:
                    cfg["tags"].extend(x for x in ["equity"] if x not in cfg["tags"])
                cfg["id"] = int(cfg["id"]) if cfg["id"] else cfg["id"]
                yield user, cfg

    def init_api(self) -> None:
        """Connect to twitter."""
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def send_status(self, status: Dict[str, str]) -> None:
        """Send user scraping status to the data store."""
        update_status(status, self.name)

    def query_twitter_api(self, is_first: bool, screen_name: str, max_id: int) -> Optional[list]:
        """Query twitter API fot new user tweets."""
        if is_first:
            return self.api.user_timeline(
                count=self.tweets_per_query,
                screen_name=screen_name,
                tweet_mode="extended",
            )
        else:
            return self.api.user_timeline(
                count=self.tweets_per_query,
                max_id=max_id - 1,
                screen_name=screen_name,
                tweet_mode="extended",
            )

    def set_forbidden(self, screen_name: str) -> None:
        """Set forbidden status."""
        log.info(f"User {screen_name} twitter is private.")
        self.send_status({"author": screen_name, "status": "forbidden"})

    def set_deleted(self, screen_name: str) -> None:
        """Set deleted status."""
        log.info(f"User {screen_name} not exist.")
        self.send_status({"author": screen_name, "status": "deleted"})

    def set_failed(self, screen_name: str) -> None:
        """Set failed status."""
        log.error(f"User {screen_name} unexpected error.")
        self.send_status({"author": screen_name, "status": "failed"})

    def get_tweets(self, screen_name: str, last_id: Optional[int]) -> Iterator:
        """Get user tweets."""
        cnt, max_id = 0, 0
        responses = {
            401: self.set_forbidden,
            404: self.set_deleted,
        }
        try:
            while 1:
                tweets = self.query_twitter_api(True if cnt == 0 else False, screen_name, max_id)
                if not tweets:
                    log.info(f"{screen_name} have no more tweets. {cnt} new tweets received.")
                    raise NoMoreTweets
                for tweet in tweets:
                    if cnt == self.max_tweets:
                        log.info(
                            f"{screen_name} Tweets limit {self.max_tweets} reached, "
                            f"scrapped {cnt} tweets.",
                        )
                        raise NoMoreTweets
                    if tweet.id == last_id:
                        log.info(f"{screen_name} post {cnt} new tweets since last scrapping.")
                        raise NoMoreTweets
                    yield tweet
                    cnt += 1
                    max_id = tweet.id
        except tweepy.error.TweepError as e:
            if e.response.status_code not in responses:
                self.set_failed(screen_name)
            responses[e.response.status_code](screen_name)
        except NoMoreTweets:
            self.send_status({"author": screen_name, "status": "active"})

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping.

        In this scrapper we use tweepy for work whit tweeter API. This method just placeholder.
        """
        yield scrapy.Request(url="https://twitter.com/", callback=self.parse)

    def get_from_status(self, status: tweepy.Status) -> Dict:
        """Collects metadata from Status object if tweet is a retweet."""
        return {
            "author": f"@{status.author.screen_name}".lower(),
        }

    def parse(self, response: TextResponse, **kwargs) -> Iterator[TweetItem]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        self.init_api()
        for user, cfg in self.twitter_users():
            if cfg["id"]:
                log.info(f"{user} last scraped tweet id - {cfg['id']}.")
            else:
                log.info(f"New user: {user}")
            for tweet in self.get_tweets(user, cfg["id"]):
                item = TweetItem()
                try:  # https://stackoverflow.com/a/55119585/4249707
                    item["text"] = tweet.retweeted_status.full_text
                    # item["meta"]["tweet_data"]["retweeted_status"] = self.get_from_status(
                    #     tweet.retweeted_status
                    # )
                    # We decided to pass tweet if it is a retweet
                    # because they are cause duplicates in DB
                    log.info("Passed %d because it's a RETWEET." % tweet.id)
                except AttributeError:
                    item["meta"] = {}
                    item["meta"]["tweet_data"] = {}
                    item["author"] = f"@{tweet.author.screen_name}".lower()
                    item["created_at"] = arrow.get(tweet.created_at).for_json()
                    item["raw"] = tweet._json
                    item["tags"] = cfg["tags"]

                    item["text"] = tweet.full_text
                    item["title"] = ""
                    item["url"] = f"https://twitter.com/{tweet.author.id}/status/{tweet.id}"
                    item["meta"]["tweet_data"][
                        "profile_image_url_https"
                    ] = tweet.author.profile_image_url_https
                    item["meta"]["tweet_data"]["id"] = tweet.id
                    item["meta"]["tweet_data"]["favorite_count"] = tweet.favorite_count
                    item["meta"]["tweet_data"]["retweet_count"] = tweet.retweet_count
                    item["meta"]["tweet_data"]["author_id"] = tweet.author.id
                    item["meta"]["tweet_data"][
                        "author_followers_count"
                    ] = tweet.author.followers_count
                    item["meta"]["tweet_data"]["author_friends_count"] = tweet.author.friends_count
                    item["meta"]["tweet_data"][
                        "author_favourites_count"
                    ] = tweet.author.favourites_count
                    item["meta"]["tweet_data"][
                        "in_reply_to_screen_name"
                    ] = tweet.in_reply_to_screen_name
                    item["meta"]["tweet_data"]["in_reply_to_user_id"] = tweet.in_reply_to_user_id
                    item["meta"]["tweet_data"]["retweeted"] = tweet.retweeted
                    item["meta"]["tweet_data"]["entities"] = tweet.entities
                    item["meta"]["tweet_data"]["lang"] = tweet.lang
                    item["meta"]["tweet_data"]["user_listed_count"] = tweet.user.listed_count

                    yield item
