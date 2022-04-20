"""Test suit for Reddit.com."""
from agblox.settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_PASSWORD, REDDIT_USERNAME
from agblox.spiders.reddit import RedditSpider
import praw
import pytest


@pytest.fixture()
def spider():
    s = RedditSpider()
    s.reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        password=REDDIT_PASSWORD,
        username=REDDIT_USERNAME,
        user_agent="reddit scraper v1.0",
    )
    s.subreddits = {
        "trademyway": {
            "status": "failed",
            "tags": ["dummy-subreddit", "data-source", "reddit", "trademyway"],
            "url": "https://www.reddit.com/r/trademyway/comments/nwxiu7/rtrademyway_lounge/",
        }
    }
    s.limit = 3
    return s


# @pytest.mark.parametrize(
#     ["expected"],
#     [
#         (["https://www.reddit.com/r/trademyway/comments/nwxpnm/lets_discuss_crypto/"],),
#     ],
# )
# def test_query_api(spider, expected, vcr_settings):
#     with vcr_settings.use_cassette("reddit.com_all_items.yaml"):
#         r = [e["url"] for e in spider.query_api(None)]
#
#     assert len(r) == 1
#     assert all([i in r for i in expected])


def test_article(spider, vcr_settings):
    with vcr_settings.use_cassette("reddit.com_article.yaml"):
        r = next(spider.query_api(None))

    assert r["author"] == "trademyway"
    assert r["created_at"] == "2021-06-10T20:32:11+00:00"
    assert r["title"] == "Let's discuss crypto"
    assert r["text"] == (
        "&#x200B;\n"
        "Comment h1mko3q: My thoughts is dummy.\n"
        "Comment h1mkw9l: What is going on.\n"
        "I can propose my solution.\n"
        "Comment h1txqgv: Anyone who stops learning is old, whether at twenty or "
        "eighty. Anyone who keeps learning stays young."
    )
    assert r["url"] == "https://www.reddit.com/r/trademyway/comments/nwxpnm/lets_discuss_crypto/"
    assert r["tags"] == ["dummy-subreddit", "data-source", "reddit", "trademyway"]


# @pytest.mark.parametrize(
#     ["expected"],
#     [
#         (
#             [
#                 "https://www.reddit.com/r/trademyway/comments/nwxpnm/lets_discuss_crypto/",
#                 "https://www.reddit.com/r/trademyway/comments/nwxiu7/rtrademyway_lounge/",
#             ],
#         ),
#     ],
# )
# def test_last_url(spider, expected, vcr_settings):
#     last_url = "https://www.reddit.com/r/wallstreetbets/comments/ojf6hh/mmat_insiders_buying_large_amount_of_shares/"
#     spider.subreddits["trademyway"]["url"] = last_url
#     with vcr_settings.use_cassette("reddit.com_last_url.yaml"):
#         r = [e["url"] for e in spider.query_api(None)]
#
#     assert len(r) == 2
#     assert r == expected
