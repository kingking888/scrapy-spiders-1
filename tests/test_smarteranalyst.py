"""Test suit for SmarterAnalystSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.smarteranalyst import SmarterAnalystSpider
import pytest


@pytest.fixture()
def spider():
    return SmarterAnalystSpider()


@pytest.fixture()
def test_kwargs():
    return {"ticker": "TWTR", "last_url": None}


headers_dict = headers(SmarterAnalystSpider.host_header)
headers_dict["User-Agent"] = SmarterAnalystSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.smarteranalyst.com/stock-page/?slug=twitter",
            headers_dict,
            [
                "https://www.smarteranalyst.com/analyst-insights/twitter-is-poised-for-an-inflection-year-says-5-star-analyst/",
                "https://www.smarteranalyst.com/yahoo/twitter-quarterly-sales-outperform-driven-by-ad-revenue-shares-rise/",
                "https://www.smarteranalyst.com/stock-news/twitter-buys-newsletter-publisher-revue/",
                "https://www.smarteranalyst.com/stock-news/twitter-settles-shareholder-derivative-lawsuits/",
                "https://www.smarteranalyst.com/stock-news/tesla-surges-to-record-putting-elon-musk-ahead-of-jeff-bezos-as-the-worlds-richest-person-report/",
                "https://www.smarteranalyst.com/stock-news/twitter-board-confident-in-leadership-structure-post-review-shares-rise/",
                "https://www.smarteranalyst.com/stock-news/twitters-ad-revenues-drive-3q-sales-beat/",
                "https://www.smarteranalyst.com/yahoo/twitter-unveils-raft-of-new-measures-ahead-of-us-elections/",
                "https://www.smarteranalyst.com/stock-news/twitter-expands-policy-to-block-misinformation-posts-ahead-of-us-election/",
                "https://www.smarteranalyst.com/stock-news/facebook-snap-held-talks-to-buy-tiktok-rival-dubsmash-report/",
                "https://www.smarteranalyst.com/stock-page/page/2/?slug=twitter",
            ],
        ),
    ],
)
def test_first_page(spider, response, test_kwargs, expected):
    r = [e.url for e in spider.parse(response=response, **test_kwargs)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.smarteranalyst.com/stock-news/facebook-snap-held-talks-to-buy-tiktok-rival-dubsmash-report/",
            headers_dict,
        ),
    ],
)
def test_article(spider, response, test_kwargs):
    r = next(spider.parse_article(response=response, **test_kwargs))
    assert (
        r["url"]
        == "https://www.smarteranalyst.com/stock-news/facebook-snap-held-talks-to-buy-tiktok-rival-dubsmash-report/"
    )
    assert (
        r["text"] == "Facebook and Snap have reportedly held talks to buy Dubsmash, a lip-syncing "
        "video app that has surged in popularity alongside rival TikTok.\n"
        "Dubsmash was approached by both Facebook (FB) and Snap about a deal in "
        "recent weeks, according to a report by The Information. The acquisition "
        "talks progressed far enough to include discussions of a price tag in the "
        "hundreds of millions of dollars. However, although the talks were ongoing in "
        "“recent weeks,” the discussions are no longer active, according to the "
        "report.\n"
        "The talks come as Microsoft Corp (MSFT) said this month that the tech giant "
        "is continuing negotiations to buy the US operations of the video-sharing app "
        "TikTok after talking to President Trump. Before the talks Trump had said "
        "that he preferred to ban the app over security concerns due to its Chinese "
        "ownership and wouldn’t support a sale. Now, Trump has given TikTok until "
        "Sept. 15 to complete sale talks or face a ban.\n"
        "Furthermore, Twitter Inc. (TWTR) has reportedly held preliminary talks to "
        "buy the US operations of TikTok. The threat by the US government to ban "
        "TikTok has increased the appeal for other large tech companies to snap up "
        "rival apps or develop their own video-sharing features and apps.\n"
        "TikTok CEO Kevin Mayer recently attacked Facebook for developing “copycat” "
        "products.\n"
        "“Facebook is even launching another copycat product, Reels (tied to "
        "Instagram), after their other copycat Lasso failed quickly,” Mayer said. "
        "“But let’s focus our energies on fair and open competition in service of our "
        "consumers, rather than maligning attacks by our competitor – namely Facebook "
        "– disguised as patriotism and designed to put an end to our very presence in "
        "the US.”\n"
        "Meanwhile Facebook is also facing scrutiny from the US government. Its CEO "
        "Mark Zuckerberg late last month provided testimony before a US congressional "
        "hearing to discuss allegations related to the dominance of the social online "
        "platform and whether the company is abusing its market power or stifling "
        "their competitors.\n"
        "Shares in Facebook have surged 27% this year as the social media network has "
        "been benefiting from a user boom during the coronavirus pandemic, which "
        "accelerated the need for remote social engagement as well as for online "
        "business and working tools.\n"
        "Looking ahead, the $287.12 average analyst price target implies shares could "
        "advance more than 10% in the coming 12 months.\n"
        "Mizuho Securities analyst James Lee this week raised the stock’s price "
        "target to $315 (21% upside potential) from $285 and maintained a Buy rating "
        "on the shares. Lee believes that the likely sale of TikTok is a positive for "
        "Facebook, as it recently launched a competitive product – Instagram Reel – "
        "to capitalize on TikTok’s uncertainty in the US.\n"
        "Overall Wall Street analysts have a bullish call on Facebook. The Strong Buy "
        "consensus boasts 31 Buy ratings versus 4 Hold ratings and 1 Sell rating. "
        "(See Facebook stock analysis on TipRanks)."
    )
    assert r["created_at"] == "2020-08-13T00:00:00+00:00"
    assert r["tags"] == ["article", "smarteranalyst", "equity", "TWTR"]
    assert r["title"] == "Facebook, Snap Held Talks To Buy TikTok Rival Dubsmash \u2013 Report"
