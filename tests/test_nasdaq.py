"""Test suit for Nasdaq."""

from agblox.spiders.helpers import headers
from agblox.spiders.nasdaq import NasdaqSpider
import pytest


@pytest.fixture()
def spider():
    return NasdaqSpider()


@pytest.fixture()
def test_kwargs():
    return {"ticker": "TWTR", "last_url": None}


headers_dict = headers(NasdaqSpider.host_header)
headers_dict["User-Agent"] = NasdaqSpider.user_agent

# CODE WAS COMMENTED BECAUSE https://www.nasdaq.com/api/v1/ IS UNREACHABLE NOW
# @pytest.mark.parametrize(
#     ["url", "headers", "expected"],
#     [
#         (
#             "https://www.nasdaq.com/api/v1/news-headlines-fetcher/TWTR/0/8",
#             headers_dict,
#             [
#                 "https://www.nasdaq.com/articles/twitter-tumblr-vimeo-push-back-against-eu-rules-on-illegal-online-content-2020-12-09",
#                 "https://www.nasdaq.com/articles/c3.ai-ipo%3A-what-investors-need-to-know-2020-12-09",
#                 "https://www.nasdaq.com/articles/why-li-auto-and-kandi-technologies-jumped-but-ciig-merger-dropped-today-2020-12-08",
#                 "https://www.nasdaq.com/articles/why-twitter-stock-gained-13-in-november-2020-12-08",
#                 "https://www.nasdaq.com/articles/bottom-fishing-and-trend-chasing%3A-exxons-writedown-and-renewable-energys-surge-2020-12-08",
#                 "https://www.nasdaq.com/articles/britains-competition-regulator-sets-out-new-regime-for-tech-giants-2020-12-08",
#                 "https://www.nasdaq.com/articles/congress-faces-christmas-showdown-with-trump-over-tech-and-defense-bill-2020-12-07",
#                 "https://www.nasdaq.com/articles/what-we-really-learned-about-amazon-shopify-and-more-on-black-friday-2020-12-07",
#                 "https://www.nasdaq.com/api/v1/news-headlines-fetcher/TWTR/100/100",
#             ],
#         ),
#     ],
# )
# def test_first_page_twtr(spider, response, expected, test_kwargs):
#     r = [e.url for e in spider.parse(response=response, **test_kwargs)]
#     assert r == expected


# @pytest.mark.parametrize(
#     ["url", "headers", "expected"],
#     [
#         (
#             "https://www.nasdaq.com/api/v1/news-headlines-fetcher/TWTR/6776/8",
#             headers_dict,
#             [
#                 "https://www.nasdaq.com/articles/social-networking-service-twitter-sets-terms-highly-anticipated-13-billion-ipo-2013-10-24",
#                 "https://www.nasdaq.com/api/v1/news-headlines-fetcher/TWTR/6876/100",
#             ],
#         ),
#     ],
# )
# def test_last_page_twtr(spider, response, expected, test_kwargs):
#     spider.offset = 6776
#     r = [e.url for e in spider.parse(response=response, **test_kwargs)]
#     assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.nasdaq.com/api/v1/news-headlines-fetcher/FSR/56/8",
            headers_dict,
            [],
        ),
    ],
)
def test_not_existed_page(spider, response, expected, test_kwargs):
    spider.offset = 56
    r = [e.url for e in spider.parse(response=response, **test_kwargs)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.nasdaq.com/articles/consumer-sector-update-for-05-17-2019%3A-wtrh-baba-amzn-trow-wmt-mcd-dis-cvs-ko-2019-05-17",
            headers_dict,
        ),
    ],
)
def test_article(spider, response, test_kwargs):
    r = next(spider.parse_article(response=response, **test_kwargs))
    assert (
        r["url"]
        == "https://www.nasdaq.com/articles/consumer-sector-update-for-05-17-2019%3A-wtrh-baba-amzn-trow-wmt-mcd-dis-cvs-ko-2019-05-17"
    )
    assert r["text"] == (
        "T op Consumer Stocks: WMT: -0.08% MCD: -0.25% DIS: -0.75% CVS: -0.38% KO: "
        "-0.52% Consumer heavyweights were declining in Friday pre-bell trade. Early "
        "movers include: (-) Waitr Holdings ( WTRH ), which was more than 4% lower "
        "after pricing a follow-on public offering of 6.76 million shares of common "
        "stock at $7.40 each, for gross proceeds of $50.0 million. (-) Alibaba Group "
        "Holding ( BABA ) was declining by more than 2% after saying an additional "
        "nine partners have joined the EMEA Ecosystem Partner Program of its cloud "
        "computing and data intelligence arm Alibaba Cloud. In other sector news: (-) "
        "Deliveroo confirmed that Amazon ( AMZN ) is leading a new $575 million "
        "Series G preferred shared funding round for the British food delivery "
        "startup, alongside existing investors T. Rowe Price ( TROW ), Fidelity "
        "Management and Research Company, and Greenoaks. Amazon was trading slightly "
        "lower pre-market. The views and opinions expressed herein are the views and "
        "opinions of the author and do not necessarily reflect those of Nasdaq, Inc."
    )
    assert r["created_at"] == "2019-05-17T09:21:50-0400"
    assert (
        r["title"]
        == "Consumer Sector Update for 05/17/2019: WTRH, BABA, AMZN, TROW, WMT, MCD, DIS, CVS, KO"
    )
