"""Models for your scraped items.

References:
    https://docs.scrapy.org/en/latest/topics/items.html
"""
from datetime import datetime, timezone
import re
from typing import List

import arrow
import dateutil.parser
from itemloaders.processors import Compose, Join, MapCompose, TakeFirst
from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import BaseType, DictType, ListType, StringType, URLType
import scrapy
from w3lib.html import remove_tags


def check_for_empty_string(input_str: str, loader_context: dict) -> str:
    """This method is used to validate the input string."""
    if not input_str:
        raise ValueError(f"Length of {loader_context['field']} cannot be 0")

    return input_str


def normalize_whitespace(txt: str) -> str:
    """This method is used to standardize how we normalize whitespace."""
    txt = txt.replace(" ", " ")  # Replace &nbsp; with a space
    txt = re.sub(r"\n+", "\n", txt)
    txt = re.sub(r"\n +", "\n", txt)
    txt = re.sub(r"[^\S\n]+", " ", txt)

    return txt.strip()


def normalize_text(txt: str) -> str:
    """Normalize each paragraph of text."""
    # paragraphs = [normalize_whitespace(i) for i in txt.split("\n \n")]
    paragraphs = [normalize_whitespace(i.strip()) for i in txt.split("\n") if i.strip()]
    txt = "\n".join([i for i in paragraphs if i])
    return txt.strip()


def clean_gads_block(txt: str) -> str:
    """Find and remove GoogleAds common used JS block."""
    txt = re.sub(r"\(adsbygoogle = window\.adsbygoogle \|\| \[]\)\.push\({}\);", "", txt)
    return txt


def _try_parsing_date(created_at_str: str, formats: List[str]) -> str:
    for fmt in formats:
        try:
            return arrow.get(created_at_str, fmt).for_json()
        except arrow.ParserError:
            pass
        except Exception:
            raise ValueError(f"Can not to convert date {created_at_str}")

    raise ValueError("Can not to convert date")


def to_iso_date(created_at_str: str, loader_context: dict) -> str:
    """This method is used to convert to iso from the given format."""
    date_format = loader_context.get("date_format")

    if date_format is None:
        # If we get it already in ISO format, there's no need to do a conversion
        return created_at_str
    formats = date_format if isinstance(date_format, list) else [date_format]
    return _try_parsing_date(created_at_str, formats)


def to_date(date_str: str) -> str:
    """This method is used to validate the created_at time."""
    date = dateutil.parser.parse(date_str).replace(tzinfo=timezone.utc)

    now = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Check if article was posted in future. Since that's impossible, it will lead to us raising an
    # exception
    if date > now:
        raise ValueError("Cannot have created_at from the future")

    return date_str


class ArticleValidateItem(Model):
    """Class for validate ArticleItem."""

    author = StringType(required=True, min_length=1)
    created_at = StringType(required=True, min_length=1)
    raw = StringType(required=True, min_length=1)
    text = StringType(required=True, min_length=1)
    title = StringType(required=True, min_length=1)
    url = URLType(required=True)
    sentiment = BaseType()
    src = StringType(min_length=1)
    tags = ListType(StringType)
    meta = DictType(StringType)


class AudioEpisodeValidateItem(ArticleValidateItem):
    """Separate class for validating audio podcast items."""

    text = StringType(required=False)


class YoutubeVideoValidateItem(ArticleValidateItem):
    """Separate class for validating Youtube video items."""

    text = StringType(required=False)


class EquityArticleValidateItem(ArticleValidateItem):
    """Class for validate EquityArticleItem."""

    meta = DictType(StringType, required=True)

    def validate_meta(self, data, value):  # noqa: ANN001 ANN201
        """Method for validate meta attribute."""
        if not value.get("base_ticker"):
            raise ValidationError("Key 'base_ticker' in meta is required")
        return value


class RedditSubredditValidateItem(ArticleValidateItem):
    """Class for validate RedditSpiderItem."""

    text = StringType(required=True, min_length=64)
    meta = BaseType(required=True)
    raw = StringType(required=False)

    def validate_meta(self, data, value):  # noqa: ANN001 ANN201
        """Method for validate meta attribute."""
        if not value.get("reddit_data"):
            raise ValidationError("Key 'reddit_data' in meta is required")
        return value


class RedditSearchValidateItem(EquityArticleValidateItem):
    """Class for validate RedditSearchItem."""

    meta = BaseType(required=True)


class GoogleTrendsValidateItem(EquityArticleValidateItem):
    """Class for validate GoogleTrendsItem."""

    meta = BaseType(required=True)
    text = StringType(required=False)


class TwitterSearchValidateItem(EquityArticleValidateItem):
    """Class for validate EquityArticleItem."""

    meta = BaseType(required=True)
    text = StringType(required=True)

    def validate_text(self, data, value):  # noqa: ANN001 ANN201
        """Method for validate meta attribute."""
        if not value.get("base_ticker"):
            raise ValidationError("Key 'base_ticker' in meta is required")
        return value


class ArticleItem(scrapy.Item):
    """Article item.

    Common item for articles spiders.
    """

    author = scrapy.Field(
        input_processor=MapCompose(normalize_whitespace),
        output_processor=Join(),
    )  # author
    created_at = scrapy.Field(
        input_processor=MapCompose(
            normalize_whitespace, check_for_empty_string, to_iso_date, to_date, field="created_at"
        ),
        output_processor=TakeFirst(),
    )  # article date
    raw = scrapy.Field(
        input_processor=MapCompose(normalize_whitespace),
        output_processor=Join(),
    )  # raw html
    src = scrapy.Field()  # link to raw data
    tags = scrapy.Field()  # item tags
    text = scrapy.Field(
        input_processor=Compose(
            Join(), remove_tags, clean_gads_block, normalize_whitespace, normalize_text
        ),
        output_processor=Join(),
    )  # article text
    title = scrapy.Field(
        input_processor=MapCompose(normalize_whitespace),
        output_processor=Join(),
    )  # article name
    sentiment = scrapy.Field()  # sentiment by topic
    url = scrapy.Field(
        input_processor=MapCompose(normalize_whitespace),
        output_processor=Join(),
    )  # article url
    meta = scrapy.Field(output_processor=TakeFirst())


class AudioEpisodeItem(ArticleItem):
    """Used for audio episode item fields."""

    text = scrapy.Field(output_processor=Join())


class YoutubeVideoItem(ArticleItem):
    """Used for Youtube video item fields."""

    text = scrapy.Field(output_processor=Join())


class EquityArticleItem(ArticleItem):
    """This class required for split validations for equity articles."""

    pass


class RedditSubredditItem(ArticleItem):
    """Class for split validations for submission searched on reddit.com started from subreddit."""

    pass


class RedditSearchItem(ArticleItem):
    """Class for split validations for submission searched on reddit.com by the ticker."""

    pass


class GoogleTrendsItem(ArticleItem):
    """Class for split validations for Google Trens page source."""

    text = scrapy.Field(output_processor=Join())


class RedditCommentsItem(scrapy.Item):
    """This class uses for updating comments from Reddit submission."""

    text_id = scrapy.Field()  # text id on datalake
    comments_text = scrapy.Field(
        input_processor=Compose(Join(), remove_tags, normalize_text, normalize_whitespace),
        output_processor=Join(),
    )  # comments messages text
    url = scrapy.Field(
        input_processor=MapCompose(normalize_whitespace),
        output_processor=Join(),
    )  # reddit comment url
    last_comment_id = scrapy.Field()


class TweetItem(scrapy.Item):
    """Twitter spider item."""

    author = scrapy.Field()  # tweet author
    created_at = scrapy.Field()  # tweet timestamp
    raw = scrapy.Field()  # raw data
    src = scrapy.Field()  # link to the stored raw data
    tags = scrapy.Field()  # item tags
    text = scrapy.Field()  # tweet text
    title = scrapy.Field()  # empty
    sentiment = scrapy.Field()  # sentiment by topic
    url = scrapy.Field()  # tweet url
    meta = scrapy.Field()  # tweet text metadata


class TickerItem(scrapy.Item):
    """Stock market ticker item."""

    close = scrapy.Field()  # ticker close value
    date = scrapy.Field()  # ticker timestamp
    dividends = scrapy.Field()
    high = scrapy.Field()  # ticker highest value
    low = scrapy.Field()  # ticker lowest value
    open = scrapy.Field()  # ticker open value
    splits = scrapy.Field()
    ticker = scrapy.Field()  # ticker name
    volume = scrapy.Field()


class GithubUserItem(scrapy.Item):
    """Github user item."""

    url = scrapy.Field(output_processor=TakeFirst())  # github user url
    meta = scrapy.Field(output_processor=TakeFirst())  # contains all user profile data
    src = scrapy.Field(output_processor=TakeFirst())  # github user src


class LinkedinItem(scrapy.Item):
    """Linkedin user item."""

    name = scrapy.Field(output_processor=TakeFirst())  # Linkedin profile name
    person_identifier = scrapy.Field(output_processor=TakeFirst())  # Linkedin profile id
    profile_id = scrapy.Field(output_processor=TakeFirst())  # Linkedin profile id
    position = scrapy.Field(output_processor=TakeFirst())  # Linkedin user position/role
    url = scrapy.Field(output_processor=TakeFirst())  # Linkedin profile url
    src = scrapy.Field(output_processor=TakeFirst())  # Path where data is stored
    tags = scrapy.Field()  # List of tags added
    meta = scrapy.Field(output_processor=TakeFirst())  # Additional data
    scraped_at = scrapy.Field(output_processor=TakeFirst())  # Linkedin user created_at
    updated_at = scrapy.Field(output_processor=TakeFirst())  # Linkedin user updated_at


class ModelDataItem(scrapy.Item):
    """Item using for S&P500 companies models."""

    def __str__(self) -> str:
        """Return an empty repr of item."""
        return ""

    data = scrapy.Field()  # scraped data
    src = scrapy.Field()  # link to a source file
    ticker = scrapy.Field()  # for holding a ticker symbol


class FinCalendarItem(scrapy.Item):
    """Item using for Financial Modeling Prep."""

    data = scrapy.Field()  # scraped data
    # url = scrapy.Field(output_processor=TakeFirst())  # scraped url
    src = scrapy.Field()  # link to a source file


class PolygonStockAggregatedItem(scrapy.Item):
    """Item for storing Polygon data from Aggregates (Bars).

    https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksTicker__range__multiplier___timespan___from___to
    """

    ticker = scrapy.Field(output_processor=TakeFirst())
    result = scrapy.Field()
