"""Test suit for Yahoo Articles."""
from agblox.spiders.helpers import headers
from agblox.spiders.yahoo_articles import YahooBaseSpider
import pytest


@pytest.fixture()
def spider():
    return YahooBaseSpider()


@pytest.fixture()
def test_kwargs():
    return {
        "ticker": "FSR",
        "tags": ["equity", "FSR", "ca.finance.yahoo.com"],
        "name": "yahoo-fsr",
    }


_headers = headers(YahooBaseSpider.name)
_headers["User-Agent"] = YahooBaseSpider.user_agent
del _headers["Host"]


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://ca.finance.yahoo.com/news/nio-stock-touches-alltime-highs-after-doubling-ev-deliveries-to-a-new-monthly-record-165054298.html",
            _headers,
        ),
    ],
)
def test_article(spider, response, test_kwargs):
    r = next(spider.parse_article(response, **test_kwargs))
    assert (
        r["url"]
        == "https://ca.finance.yahoo.com/news/nio-stock-touches-alltime-highs-after-doubling-ev-deliveries-to-a-new-monthly-record-165054298.html"
    )
    assert (
        r["text"]
        == "Chinese electric car maker NIO ( NIO ) hit all-time intraday highs on Monday after doubling "
        "its deliveries in October to a new monthly record. NIO delivered 5,055 vehicles in October, "
        "an increase of 100% year-over-year. In 2020 deliveries jumped to 31,430 vehicles, a 111.4% "
        "spike compared to last year. Investors have been pleased with the Chinese rival to Tesla "
        "( TSLA ) which is set to report its quarterly results on November 17th. Year-to-date NIO\u2019s "
        "American depository shares are up around 740%. It\u2019s not surprising to see the company\u2019s "
        "shares spike by double-digit percentages following monthly delivery results or analyst "
        "upgrades. In October, JPMorgan upgraded the stock to Overweight , sending the stock up 22% "
        "that day. Analyst Nick Lai admitted he missed the stock\u2019s major rally year to date, and "
        "said, \u201cNIO remains attractive from a long term perspective.\u201d In July shares surged "
        "22% during one session after reporting a whopping 179% for its June sales. Since the pandemic, "
        "NIO has secured funding and received cash infusions which \u201chave largely removed any "
        "liquidity risk for the company between now and our expected break-even in 2022E,\u201d "
        "Goldman analyst Fei Fang wrote over the summer . A NIO EP9 electric car is displayed at "
        "its store in Beijing, China August 20, 2020. REUTERS/Tingshu Wang Two other electric "
        "vehicle startups are also soaring on Monday. Shares of Chinese EV startup Xpeng ( XPEV ), "
        "which went public over the summer, are also higher following its October delivery numbers. "
        "XPeng delivered 3,040 vehicles in October , an increase of 229% year-over-year. American EV "
        "start-up Fisker ( FSR ) is also up around 16% today after gaining 13% on Friday when it "
        "debuted on the New York Stock Exchange via a special purpose acquisition company, or SPAC. "
        "Ines covers the U.S. stock market. Follow her on Twitter at @ines_ferre Why Tesla would be "
        "one of the biggest EV pure play winners if Biden gets elected: Analyst Tesla bull says "
        "long-term thesis 'still intact,' sees $7,000 price target by 2024 Bearish Tesla analyst "
        "explains why shares could surge to $2,070 Story continues NIO share price reflects "
        "'over-optimism': Goldman Tesla\u2019s most bullish analyst sets a Street-high price "
        "target of $2,322 Follow Yahoo Finance on Twitter , Facebook , Instagram , Flipboard , "
        "LinkedIn , and reddit ."
    )
    assert r["created_at"] == "2020-11-02T16:50:54.000Z"
    assert (
        r["title"]
        == "NIO stock touches all-time highs after doubling EV deliveries to a new monthly record"
    )
    assert r["tags"] == test_kwargs["tags"]
    assert r["meta"]["base_ticker"] == "FSR"
