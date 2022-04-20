"""Test suit for AgfaxSpider."""

from agblox.spiders.agfax import AgfaxSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return AgfaxSpider()


headers = headers(AgfaxSpider.name)
headers["User-Agent"] = AgfaxSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://agfax.com/tag/corn-news/",
            headers,
            [
                "https://agfax.com/2020/10/08/dtn-grain-open-markets-press-higher-in-early-trade/",
                "https://agfax.com/2020/10/07/dtn-grain-closing-grains-at-new-high/",
                "https://agfax.com/2020/10/07/corn-soybean-price-changes-and-relative-profitability/",
                "https://agfax.com/2020/10/07/illinois-corn-now-is-not-the-time-to-scout-for-diseases/",
                "https://agfax.com/2020/10/07/dtn-grain-midday-all-grains-higher-9/",
                "https://agfax.com/2020/10/07/texas-field-reports-pumpkin-yields-down-quality-up/",
                "https://agfax.com/2020/10/07/dtn-grain-open-corn-leads-mostly-higher-trade/",
                "https://agfax.com/2020/10/06/minnesota-considerations-for-corn-harvest-podcast/",
                "https://agfax.com/2020/10/06/webinar-corn-soybean-outlook-oct-9/",
                "https://agfax.com/tag/corn-news/page/2/",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://agfax.com/tag/corn-news/page/996/",
            headers,
            [
                "https://agfax.com/2014/04/01/brazil-corn-top-state-see-32-percent-production-decline-dtn/",
                "https://agfax.com/2014/02/25/corn-4-grain-companies-reject-traits-approved-china-dtn/",
                "https://agfax.com/2014/02/18/corns-glory-years-bypassed-many-farmers-survey-finds-dtn/",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://agfax.com/2020/10/08/dtn-grain-open-markets-press-higher-in-early-trade/",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["url"]
        == "https://agfax.com/2020/10/08/dtn-grain-open-markets-press-higher-in-early-trade/"
    )
    assert (
        r["text"]
        == """Pre-6 a.m. Globex Prices: December corn is up 3 cents, November soybeans are up 7 cents and December KC wheat is up 6 1/2 cents. CME Globex Recap: Early Thursday, Dow Jones futures are trading modestly higher with several media sources reporting talks are continuing on a possible limited version of a coronavirus relief bill that would extend help to the airlines industry. Hopes for a larger bill were cut short Tuesday by a presidential tweet. The December U.S. dollar index is trading slightly lower and commodities are starting the day mixed to higher. At 7:30 a.m. CDT, USDA will release its weekly export sales report and traders will remain especially interested in the status of soybean and pork sales to China. OUTSIDE MARKETS: Previous closes on Wednesday showed the Dow Jones Industrial Average up 530.70 at 28,303.46 and the S&P 500 up 58.50 at 3,419.45 while the 10-Year Treasury yield ended at 0.78%. Early Thursday, December Dow Jones futures are up 107 points. Asian markets are higher with Japan’s Nikkei 225 up 224.25 (1.0%) and China’s Shanghai Composite closed for national holiday. European markets are mixed with London’s FTSE 100 down 11.02 points (-0.2%), Germany’s DAX up 35.52 points (0.3%) and France’s CAC 40 down 1.51 points (-0.01%). The December euro is down $.0009 at $1.1775. The December U.S. Dollar Index is down 0.04 at 93.64. The December 30-year T-bond is up 13/32nds, while December gold is up $5.90 at $1,896.70 and November crude oil is up $0.44 at $40.39. China’s Dalian Exchange was closed for national holiday Thursday. November palm oil is trading up 0.8% at 2,892 ringgits, but is still below the 2020 high of 3,150 ringgits."""
    )
    assert r["created_at"] == "2020-10-08T06:58:17-05:00"
    assert r["title"] == "DTN Grain Open: Markets Press Higher in Early Trade"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://agfax.com/2020/10/07/dtn-grain-open-corn-leads-mostly-higher-trade",
            headers,
        ),
    ],
)
def test_article_date_not_updated(spider, response):
    r = next(spider.parse_article(response))
    assert r["created_at"] == "2020-10-07T06:54:07-05:00"


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://agfax.com/tag/corn-news/",
            headers,
            [
                "https://agfax.com/2020/10/08/dtn-grain-open-markets-press-higher-in-early-trade/",
                "https://agfax.com/2020/10/07/dtn-grain-closing-grains-at-new-high/",
                "https://agfax.com/2020/10/07/corn-soybean-price-changes-and-relative-profitability/",
            ],
        ),
    ],
)
def test_limit(response, expected):
    spider = AgfaxSpider()
    spider.last_url = (
        "https://agfax.com/2020/10/07/illinois-corn-now-is-not-the-time-to-scout-for-diseases/"
    )
    r = [e.url for e in spider.parse(response)]
    assert r == expected
