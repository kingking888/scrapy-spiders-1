"""Test suit for ForexEmpire."""

from agblox.spiders.forex_empire import ForexEmpireSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return ForexEmpireSpider()


headers_dict = headers(ForexEmpireSpider.host_header)
headers_dict["User-Agent"] = ForexEmpireSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            ForexEmpireSpider.url,
            headers_dict,
            [
                "https://www.fxempire.com/corona-virus",
                "https://www.fxempire.com/widgets/corona-virus",
                "https://www.fxempire.com/corona-virus",
                "https://www.fxempire.com/news/forex-news?page=2",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.fxempire.com/news/forex-news?page=196",
            headers_dict,
            [
                "https://www.fxempire.com/corona-virus",
                "https://www.fxempire.com/widgets/corona-virus",
                "https://www.fxempire.com/corona-virus",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.fxempire.com/forecasts/article/audusd-forex-technical-analysis-risk-off-scenario-triggered-by-north-korean-missile-launch-437278",
            headers_dict,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == r"""The AUD/USD is trading lower early Friday as investors shed risky assets following the North Korean launching of another ballistic missile over Japan. The Aussie could break even further if global investors decide that this is a major issue. Given their response to previous North Korean missile launches, the negative effect on the currency could be minimal. On Thursday, the AUD/USD posted a dramatic rebound rally in response to the U.S. consumer inflation data. Although the data indicated inflation growth, traders reacted as if the news wasn’t strong enough to shift Fed sentiment from dovish to hawkish. Daily AUDUSD Technical Analysis The main trend is up according to the daily swing chart. However, momentum had been trending lower since September 8. Yesterday’s closing price reversal bottom may have shifted momentum back to the upside. We can confirm this when buyers take out .8016. The main range is .7807 to .8124. Its retracement zone at .7065 to .7928 stopped the selling on Thursday when the Aussie reached its low at .7955. The short-term range is .8124 to .7955. If buyers can take out .8016 and confirm the closing price reversal bottom at .7955 then we should see a rally into its retracement zone at .8040 to .8060. Forecast Based on the current price at .7988 (0352 GMT), the direction of the AUD/USD the rest of the session will be determined by trader reaction to an uptrending angle at .7981. A sustained move over .7981 will signal the presence of buyers. This could generate enough upside momentum to challenge the downtrending angle at .8024. Watch for a technical bounce on the first test of this angle. Taking out .8024 with conviction could trigger a rally into the short-term retracement zone at .8040 to .8060. This is followed by the downtrending angle at .8074. A sustained move under .7981 will indicate the presence of sellers. The first target is the 50% level at .7965. This is followed by the closing price reversal bottom at .7955 and a support cluster at .7928 to .7922. Basically, we’re looking for a strong upside bias to develop on a sustained move over .8024 and a bearish bias to develop on a sustained move under .7981."""
    )
    assert r["created_at"] == "2017-09-15T04:05:15+00:00"
    assert r["tags"] == ["FOREX", "article", "fxempire.com"]
    assert (
        r["title"]
        == "AUD/USD Forex Technical Analysis – Risk Off Scenario Triggered by North Korean Missile Launch"
    )
