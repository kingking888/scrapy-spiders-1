"""Test suit for MarketWatch."""

from agblox.spiders.helpers import headers
from agblox.spiders.marketwatch import MarketWatchSpider
import pytest


@pytest.fixture()
def spider():
    return MarketWatchSpider()


@pytest.fixture()
def test_kwargs():
    return {
        "ticker": "AMZN",
        "last_url": None,
        "page": 0,
        "timestamp": "Jan. 11, 2021 at 0:00 a.m. ET",
    }


headers = headers(MarketWatchSpider.host_header)
headers["User-Agent"] = MarketWatchSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.marketwatch.com/investing/stock/AMZN/moreheadlines?channel=MarketWatch&pageNumber=0",
            headers,
            [
                "https://www.marketwatch.com/story/the-jedi-reboot-allows-u-s-to-correct-its-mistake-11625687703",
                "https://www.marketwatch.com/story/zevia-ipo-5-things-to-know-about-the-zero-calorie-beverage-company-before-it-goes-public-11625592545",
                "https://www.marketwatch.com/story/why-economists-think-bond-yields-are-falling-slamming-the-s-p-500-and-the-dow-as-the-likes-of-amazon-benefit-11625743122",
                "https://www.marketwatch.com/story/amazon-com-inc-stock-outperforms-market-on-strong-trading-day-01625689840-541041c9ce32",
                "https://www.marketwatch.com/articles/big-tech-stocks-risk-funds-51625257865",
                "https://www.marketwatch.com/articles/amc-didi-big-tech-stock-market-today-51625661767",
                "https://www.marketwatch.com/articles/things-to-know-today-51625658757",
                "https://www.marketwatch.com/articles/the-dow-dropped-200-points-tuesday-dont-blame-didi-and-opec-51625605922",
                "https://www.marketwatch.com/story/stock-futures-pause-for-breath-with-s-p-500-nasdaq-at-records-11625570766",
                "https://www.marketwatch.com/story/amazon-com-inc-stock-outperforms-market-on-strong-trading-day-01625603436-a81d102a7466",
                "https://www.marketwatch.com/story/amazon-stock-rides-to-record-as-jedi-deal-gets-cancelled-on-new-ceos-first-day-11625602173",
                "https://www.marketwatch.com/articles/microsoft-jedi-defense-contract-amazon-51625596606",
                "https://www.marketwatch.com/articles/amazon-stock-all-time-high-51625585152",
                "https://www.marketwatch.com/articles/alphabet-stock-discount-51625588865",
                "https://www.marketwatch.com/story/pentagon-abruptly-cancels-10-billion-jedi-cloud-contract-11625590861",
                "https://www.marketwatch.com/story/amazon-adds-more-than-100-billion-in-market-cap-in-2-days-2021-07-06",
                "https://www.marketwatch.com/articles/amazon-ceo-jeff-bezos-andy-jassy-51625253171",
                "https://www.marketwatch.com/articles/levi-strauss-earnings-51625259738",
                "https://www.marketwatch.com/articles/things-to-know-today-51625572525",
                "http://www.marketwatch.com/articles/amazon-thursday-night-football-nfl-1505509977",
                "https://www.marketwatch.com/investing/stock/AMZN/moreheadlines?channel=MarketWatch&pageNumber=1",
            ],
        ),
    ],
)
def test_first_page(spider, response, test_kwargs, expected):
    links = [e.url for e in spider.parse(response=response, **test_kwargs)]
    assert links == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.marketwatch.com/articles/dow-jones-industrial-average"
            "-fell-stock-profits-ripe-to-take-51610402230",
            headers,
        ),
    ],
)
def test_article(spider, response, test_kwargs):
    r = next(spider.parse_article(response=response, **test_kwargs))
    assert (
        r["text"] == "Stocks fell Monday after last week. Tech stocks got it the worst. The\n"
        "fell 89.28 points, or 0.29%, to close at 31,008.69. The\n"
        "fell 25.07 points, or 0.66%, to end at 3,799.61, and the\n"
        "fell 165.54 points, or 1.25% to close at 13,036.43. The biggest gainer on "
        "the S&P 500 was\n"
        "(ticker: LLY) up 12% after from a Phase 3 trial of its Alzheimer’s drug. It "
        "was growth and technology stocks leading the way down. As optimism on the "
        "trajectory of the U.S. economy—powered by —is sustained, investors continue "
        "to favor economically sensitive value stocks over growth. The\n"
        "fell 1.2%, while its\n"
        "(VOOV) slipped just 0.02%. The\n"
        "fell 1%. First off,\n"
        "(TWTR) 6.4% after banning President Donald Trump’s account. The President "
        "has roughly 88 million followers and analyst Crag Huber at Huber Research "
        "Partners tells some are assuming roughly 12 million to 15 million daily "
        "active users leave the platform. That’s about 6% to 8% of Twitter’s total "
        "187 million daily active users, potentially justifying the stock’s reaction, "
        "which doesn’t necessarily account for any changes in profit margins. But "
        "Twitter doesn’t move the major indexes like\n"
        "(APPL)—worth $2.2 trillion and down 2.3%—does. Twitter’s market "
        "capitalization is just $38 billion. The point is that growth stocks across "
        "the board were having a rough day and rising interest rates—which is "
        "consistent with firming economic and inflation expectations—may be eating "
        "into appetite for growth stocks. Higher rates eat into corporate cash flows— "
        ". The 10-year treasury yield has in the past several trading sessions. "
        "Still, rates may need to go to before materially affecting stock valuations. "
        "Overall, stock prices are indeed quite extended. Sure, value stocks "
        "outperformed Monday, but not spectacularly. About 92% of S&P 500 stocks "
        "entered the day trading above their 200-day moving averages, which indicates "
        "the market is “very overextended,” according to a note from strategists at "
        "Morgan Stanley. Stocks haven’t traded in that territory since 2013, they "
        "wrote. Investors have in fact been willing to to own stocks as fear of "
        "economic uncertainty eases. In that light, Monday’s fall was "
        "“profit-taking,” Tim Courtney, chief investment officer at Exencial Wealth "
        "Advisors, told . “We’re going to start having more days like this as the "
        "market has priced itself for everything to work out.” More days like this "
        "certainty holds stocks back for the near-term, but Morgan Stanley did point "
        "out that at these levels, stocks can still eke out gains for the next "
        "several months. In the grand scheme of things, vaccine-distribution "
        "questions are running up against a forward-earnings picture that has already "
        "brightened in recent months. Next on investors’ radars: fourth-quarter "
        "earnings and guidance, the latter hopefully adjusted higher. Jacob "
        "Sonenshine at"
    )
    assert r["created_at"] == "2021-01-11T00:00:00+00:00"
    assert r["tags"] == ["marketwatch", "article", "equity", "AMZN"]
    assert r["title"] == "The Dow Fell 89 Points Because Stocks Are Way Overextended"
    assert r["meta"]["base_ticker"] == test_kwargs["ticker"]
