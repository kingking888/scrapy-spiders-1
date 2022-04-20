"""Reddit spider."""
from datetime import datetime, timezone
import importlib.metadata
import logging
from typing import Dict, Iterator, List, Optional

from agblox.items import RedditSubredditItem
from agblox.settings import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_PASSWORD,
    REDDIT_USERNAME,
    YURI,
)
from agblox.spiders.helpers import BaseSpider, update_status
import praw
from praw.exceptions import PRAWException
from praw.models import MoreComments, Submission
from praw.models.comment_forest import CommentForest
from prawcore.exceptions import Redirect
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class LimitReached(Exception):
    """Used for catching the last scraped post."""

    pass


class RedditSpider(BaseSpider):
    """Spider for reddit.com site."""

    name: str = "reddit.com"
    host_header = "www.reddit.com"
    spider_author = YURI
    limit = 1000  # for test fixtures used 3

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping.

        This method just placeholder.
        """
        proj_meta = importlib.metadata.metadata("agblox")
        self.crawler.stats.set_value("droped_items_with_comments", 0)
        self.crawler.stats.set_value("droped_items_comments_total", 0)
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            password=REDDIT_PASSWORD,
            username=REDDIT_USERNAME,
            user_agent=f"script:{proj_meta['Name']}.example.redditapp:{proj_meta['Version']} "
            f"(by u/{REDDIT_USERNAME})",
        )
        self.subreddits = self.cfg["subreddits"]

        yield scrapy.Request(
            url="https://www.reddit.com/",
            callback=self.query_api,
        )

    def query_api(self, response: TextResponse, **kwargs) -> Iterator[RedditSubredditItem]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        subreddits = [
            k for k, v in self.subreddits.items() if v["status"] in ["active", "new", "failed"]
        ]

        for sub_name in subreddits:
            try:
                for submission in self.reddit.subreddit(sub_name).new(
                    limit=self.limit  # 1000 is the max which Reddit allow to get for one subreddit
                ):
                    if not submission.url.startswith("https://www.reddit.com"):
                        continue
                    if submission.url == self.subreddits[submission.subreddit.display_name]["url"]:
                        log.info(f"Limit reached for subreddit: {sub_name}.")
                        raise LimitReached
                    item = self.add_item(
                        submission,
                        submission.subreddit.display_name,
                        self._gen_tags_for_submission(sub_name),
                    )
                    if item is not None:
                        yield item
                self.send_status({"author": sub_name, "status": "active"})
            except Redirect:
                log.info(f"An attempt to crawl non-existed subreddit: {sub_name}, We passed it.")
            except PRAWException:
                self.set_failed(sub_name)
            except LimitReached:
                self.send_status({"author": sub_name, "status": "active"})

    def bound_together(self, text: str, comments: CommentForest) -> tuple:
        """Bound top level comments to the bottom of the text."""
        if len(text) < 3:
            self.crawler.stats.inc_value("droped_items_with_comments")
        all_comments = comments.list()
        for top_level_comment in all_comments:
            if len(text) < 3:
                self.crawler.stats.inc_value("droped_items_comments_total")
            if isinstance(top_level_comment, MoreComments):
                continue
            text += f"\nComment {top_level_comment.id}: {top_level_comment.body}"
        try:
            last_id = all_comments.pop().id
        except IndexError:
            last_id = None
        return text, last_id

    def add_item(
        self, item: Submission, subreddit: str, tags: List
    ) -> Optional[RedditSubredditItem]:
        """Method for add item to ItemLoader."""
        try:
            loader = ItemLoader(item=RedditSubredditItem())
            text, last_comment_id = self.bound_together(item.selftext, item.comments)
            loader.add_value("text", text)
            loader.add_value("author", subreddit)
            loader.add_value("title", item.title)
            loader.add_value("url", item.url)
            loader.add_value("raw", item.selftext_html if item.selftext_html else " ")
            loader.add_value("tags", tags)
            created_at = datetime.utcfromtimestamp(item.created_utc).replace(tzinfo=timezone.utc)
            loader.add_value("created_at", created_at.isoformat())

            try:
                post_data = {
                    "subreddit": subreddit,
                    "reddit_data": {
                        "post_author": item.author.name if item.author else "UNKNOWN",
                        "last_comment_id": last_comment_id,
                        "submission_id": item.id,
                    },
                }
            except Exception as e:
                log.info(f"Some attributes from submission may not be collected. Error: {e}")
            loader.add_value("meta", post_data)

            return loader.load_item()
        except Exception:
            log.error(f"Was problem with: {item.url}", exc_info=True)
            pass

    def send_status(self, status: Dict[str, str]) -> None:
        """Send subreddit scraping status to the data store."""
        update_status(status, self.name)

    def set_failed(self, sub_name: str) -> None:
        """Set failed status."""
        log.error(f"Subreddit {sub_name} unexpected error.")
        self.send_status({"author": sub_name, "status": "failed"})

    def _gen_tags_for_submission(self, sub: str) -> List:
        """Tags generated from recieved configuration."""
        default_tags = self.subreddits[sub]["tags"]
        if "reddit" not in default_tags:
            default_tags.append("reddit")
        return default_tags
