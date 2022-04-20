"""Reddit comments spider."""
import logging
import time
from typing import Dict, Iterator, List, Optional

from agblox.items import RedditCommentsItem
from agblox.settings import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_PASSWORD,
    REDDIT_USERNAME,
    YURI,
)
from agblox.spiders.helpers import BaseSpider
import praw
from praw.reddit import Submission
from prawcore.exceptions import Forbidden, ServerError
import scrapy
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class RedditCommentsSpider(BaseSpider):
    """Spider for comments on Reddit."""

    name: str = "reddit_comments"
    host_header = "www.reddit.com"
    spider_author = YURI

    custom_settings = {
        "ITEM_PIPELINES": {
            "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 300,
            "agblox.pipelines.FSCommentsPipeline": 310,
            "agblox.pipelines.S3CommentsPipeline": 320,
            "agblox.pipelines.APICommentsPipeline": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        }
    }

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping.

        This method just placeholder.
        """
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            password=REDDIT_PASSWORD,
            username=REDDIT_USERNAME,
            user_agent="DiviAIApp/0.1.0 by /u/yugritsai email: yugritsai@gmail.com",
        )
        self.submissions = self.cfg["meta"]["submissions"]

        yield scrapy.Request(
            url="https://www.reddit.com/",
            callback=self.query_api,
            meta={"handle_httpstatus_list": [503]},
        )

    def query_api(self, response: TextResponse, **kwargs) -> None:
        """Downloads given submission and get all top-level comments.

        If last_comment_id provided comments will be collected started from it.
        """
        for key, val in self.submissions.items():
            last_id = val.get("last_comment_id")

            try:
                submission = self.reddit.submission(id=key)
            except Forbidden:
                log.info(
                    f"Can't access comments for submission: {key}. Continue to the next one..."
                )
                continue

            try:
                submission.comments.replace_more(limit=None)
            except (AssertionError, ServerError) as e:
                log.info(f"Got an error but will try to retry. Error: {e}")
                time.sleep(5)  # wait a bit and retry
                submission.comments.replace_more(limit=None)
            except Exception as e:
                log.warning(f"Something wrong with submission request: {key}. Error: {e}")

            try:
                comment_queue = submission.comments.list()
                item = self.parse_comments_queue(
                    comment_queue, last_id=last_id, submission=submission, val=val
                )
                if item is not None:
                    yield item
            except Forbidden:
                log.info(
                    f"Can't access comments for submission: {key}. Continue to the next one..."
                )
                continue

        log.info(
            f"Total reddit submissions are {len(self.submissions.items())}. "
            f"The status code is {response.status}"
        )

    def parse_comments_queue(
        self, comment_queue: List, last_id: Optional, submission: Submission, val: Dict
    ) -> RedditCommentsItem:
        """Extracts all comments from queue, bound them with text and yields."""
        comments = []
        ids_list = [com.id for com in comment_queue]
        try:
            idx = ids_list.index(last_id)
            log.info(
                f"Submission: ({submission.id}) - Found last comment id: ({comment_queue[idx].id})"
            )
        except ValueError:
            idx = None

        if idx is not None and last_id:
            idx += 1  # for pass the last comment already scraped
        for top_level_comment in comment_queue[idx:]:
            log.info(f"Submission: ({submission.id}) - Comments body: {top_level_comment.body}")
            comments.append(top_level_comment)

        if not comments:
            log.info(f"Submission: ({submission.id}) - No new comments.")
        item = self.bound_comments(
            comments, submission_url=submission.url, text_id=val.get("text_id")
        )
        return item

    def bound_comments(self, comments: List, **kwargs) -> Optional[RedditCommentsItem]:
        """Bound top level comments to the bottom of the text."""
        if comments:
            comments_text = ""
            for com in comments:
                comments_text += f"\nComment {com.id}: {com.body}"
            try:
                last_id = comments.pop().id
            except IndexError:
                last_id = None
            kwargs["last_comment_id"] = last_id
            return self.add_item(comments_text, **kwargs)

    def add_item(self, comments_text: str, **kwargs) -> Optional[RedditCommentsItem]:
        """Method for add item to ItemLoader."""
        try:
            loader = ItemLoader(item=RedditCommentsItem())
            loader.add_value("text_id", kwargs["text_id"])
            loader.add_value("comments_text", comments_text)
            loader.add_value("url", kwargs["submission_url"])
            loader.add_value("last_comment_id", kwargs["last_comment_id"])

            return loader.load_item()
        except Exception:
            log.error(f"Was problem with submission: {kwargs['submission_url']}", exc_info=True)
            pass
