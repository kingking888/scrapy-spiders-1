"""Test suit for Reddit.com."""
from agblox.settings import (
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
)
from agblox.spiders.twitter import TwitterSpider
import pytest
import tweepy


@pytest.fixture()
def spider():
    s = TwitterSpider()
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    s.api = tweepy.API(auth)
    s.cfg = {
        "@elonmusk": {
            "id": "1372826575293583366",
            "status": "new",
            "tags": ["tesla", "twitter", "data-source", "@elonmusk"],
        }
    }
    s.get_cfg = s.cfg
    return s


def test_spider_crawl(spider):
    pass
