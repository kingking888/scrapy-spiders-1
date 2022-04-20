"""Test suit for MorningStarSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.morningstar import MorningStarSpider
import pytest


@pytest.fixture()
def spider():
    return MorningStarSpider()


@pytest.fixture()
def test_kwargs():
    return {"last_url": None}


headers = headers(MorningStarSpider.host_header)
headers["User-Agent"] = MorningStarSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://newsroom.morningstar.com/newsroom/news-archive/press-release-details/"
            "2021/Morningstar-Reports-U.S.-Mutual-Fund-and-Exchange-Traded-Fund-Flows-for-May-2021/default.aspx",
            headers,
        ),
    ],
)
def test_article(spider, response, test_kwargs):
    r = next(spider.parse_article(response, **test_kwargs))
    assert (
        r["url"]
        == "https://newsroom.morningstar.com/newsroom/news-archive/press-release-details/2021/"
        "Morningstar-Reports-U.S.-Mutual-Fund-and-Exchange-Traded-Fund-Flows-for-May-2021/default.aspx"
    )
    assert (
        r["text"] == "CHICAGO, June 15, 2021 /PRNewswire/ -- (Nasdaq: MORN), a leading "
        "provider of independent investment research, today reported "
        "estimated U.S. mutual fund and exchange-traded fund (ETF) flows for "
        "May 2021. Long-term mutual funds and ETFs collected $83 billion "
        "during May, materially less than their $156 billion haul in March "
        "and $124 billion intake in April. Investors continued to favor "
        "passively managed strategies, pouring $71 billion into "
        "index-tracking funds. Morningstar's report about U.S. fund flows for "
        "May 2021 is available . Additional highlights from the report "
        "include: The information contained herein: (1) is proprietary to "
        "Morningstar and/or its content providers; (2) may not be copied or "
        "distributed outside the scope of this press release; and (3) is not "
        "warranted to be accurate, complete, or timely. Neither Morningstar "
        "nor its content providers are responsible for any damages or losses "
        "arising from any use of this information. Past performance is no "
        "guarantee of future results.\n"
        "Morningstar, Inc. is a leading provider of independent investment "
        "research in North America, Europe, Australia, and Asia. The Company "
        "offers an extensive line of products and services for individual "
        "investors, financial advisors, asset managers and owners, retirement "
        "plan providers and sponsors, and institutional investors in the debt "
        "and private capital markets. Morningstar provides data and research "
        "insights on a wide range of investment offerings, including managed "
        "investment products, publicly listed companies, private capital "
        "markets, debt securities, and real-time global market data. "
        "Morningstar also offers investment management services through its "
        "investment advisory subsidiaries, with approximately $244 billion in "
        "assets under advisement and management as of March 31, 2021. The "
        "Company has operations in 29 countries. For more information, visit "
        ". Follow Morningstar on Twitter @MorningstarInc.\n"
        "©2021 Morningstar, Inc. All Rights Reserved. MORN-R\n"
        ": Erin Parro,\n"
        "View original content to download multimedia: SOURCE Morningstar, "
        "Inc."
    )
    assert r["created_at"] == "2021-06-15 00:00:00+00:00"
    assert (
        r["title"]
        == "Morningstar Reports U.S. Mutual Fund and Exchange-Traded Fund Flows for May 2021"
    )
    assert r["tags"] == ["article", "morningstar.com"]
