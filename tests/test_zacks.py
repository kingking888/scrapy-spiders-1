"""Test suit for ZacksSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.zacks import ZacksSpider
import pytest


@pytest.fixture()
def spider():
    return ZacksSpider()


@pytest.fixture()
def test_kwargs():
    return {"ticker": "WTRH", "last_url": None}


headers = headers("www.zacks.com")
headers["User-Agent"] = ZacksSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            ZacksSpider.create_url(ticker="WTRH"),
            headers,
            [
                "https://www.zacks.com/stock/news/1230325/tech-tops-in-2020-etfs-stocks-that-more-than-doubled",
                "https://www.zacks.com/stock/news/1205567/6-tech-stocks-that-have-crushed-nasdaq-in-2020",
                "https://www.zacks.com/stock/news/1150883/will-waitr-wtrh-gain-on-rising-earnings-estimates",
                "https://www.zacks.com/stock/news/1110787/Waitr-Holdings-WTRH-in-Focus-Stock-Moves-67-Higher",
                "https://www.zacks.com/stock/news/1099217/Waitr-Holdings-WTRH-Q3-Earnings-Surpass-Estimates",
                "https://www.zacks.com/stock/news/1092368/Waitr-Holdings-WTRH-to-Report-Q3-Results-Wall-Street-Expects-Earnings-Growth",
                "https://www.zacks.com/stock/news/1062739/Is-the-Options-Market-Predicting-a-Spike-in-Waitr-WTRH-Stock",
                "https://www.zacks.com/stock/news/831902/Company-News-for-Mar-24-2020",
                "https://www.zacks.com/stock/news/555847/The-Zacks-Analyst-Blog-Highlights-Grubhub-Uber-Waitr-and-McDonalds",
                "https://www.zacks.com/stock/news/554525/Grubhub-Banks-on-Partnerships-to-Steer-Away-Competition",
                "https://www.zacks.com/stock/news/484687/Is-the-Options-Market-Predicting-a-Spike-in-Waitr-WTRH-Stock",
                "https://www.zacks.com/stock/news/434330/Grubhub-Loses-1-Spot-in-US-Online-Food-Delivery-Market",
                "https://www.zacks.com/stock/news/428134/GrubHub-GRUB-Stock-Rises-as-News-Hits-of-Amazon-AMZN-Restaurants-Closing",
                "https://www.zacks.com/stock/news/421247/Moving-Average-Crossover-Alert-Waitr",
                "https://www.zacks.com/stock/research/WTRH/all-news?page=2&t=WTRH",
            ],
        ),
    ],
)
def test_page(spider, response, test_kwargs, expected):
    r = [e.url for e in spider.parse(response=response, **test_kwargs)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.zacks.com/stock/research/TWTR/all-news?page=64&t=TWTR",
            headers,
        ),
    ],
)
def test_last_page(spider, response, test_kwargs):
    r = [e.url for e in spider.parse(response=response, **test_kwargs)]
    assert len(r) == 0


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        ("https://www.zacks.com/stock/news/421247/moving-average-crossover-alert-waitr", headers),
    ],
)
def test_created_at(spider, response, test_kwargs):
    r = next(spider.parse_article(response=response, **test_kwargs))
    assert r["created_at"] == "2019-05-29T00:00:00+00:00"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.zacks.com/stock/news/1062739/is-the-options-market-predicting-a-spike-in-waitr-wtrh-stock",
            headers,
        ),
    ],
)
def test_text_only(spider, response, test_kwargs):
    r = next(spider.parse_article(response=response, **test_kwargs))
    assert r["text"] == (
        "Investors in Waitr Holdings Inc. ( WTRH Quick Quote WTRH - Free Report ) need"
        " to pay close attention to the stock based on moves in the options market lately."
        " That is because the Oct 16, 2020 $7.50 Call had some of the highest implied volatility"
        " of all equity options today. What is Implied Volatility? Implied volatility shows how "
        "much movement the market is expecting in the future. Options with high levels of implied "
        "volatility suggest that investors in the underlying stocks are expecting a big move in one"
        " direction or the other. It could also mean there is an event coming up soon that may"
        " cause a big rally or a huge sell-off. However, implied volatility is only one piece of "
        "the puzzle when putting together an options trading strategy. What do the Analysts Think?"
        " Clearly, options traders are pricing in a big move for Waitr shares, but what is the "
        "fundamental picture for the company? Currently, Waitr is a Zacks Rank #3 (Hold) in the "
        "Internet - Software industry that ranks in the Bottom 31% of our Zacks Industry Rank. "
        "Over the last 60 days, no analysts have increased their earnings estimates for the "
        "current quarter, while one analyst has revised the estimate downward. The net effect has "
        "taken our Zacks Consensus Estimate for the current quarter from 4 cents per share to 3 "
        "cents in that period. Given the way analysts feel about Waitr right now, this huge "
        "implied volatility could mean there\u2019s a trade developing. Oftentimes, "
        "options traders look for options with high levels of implied volatility to sell premium. "
        "This is a strategy many seasoned traders use because it captures decay. At expiration, "
        "the hope for these traders is that the underlying stock does not move as much as "
        "originally expected. Looking to Trade Options? Check out the simple yet high-powered "
        "approach that Zacks Executive VP Kevin Matras has used to close recent double and "
        "triple-digit winners. In addition to impressive profit potential, these trades can "
        "actually reduce your risk. Click to see the trades now >>"
    )


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.zacks.com/stock/news/831902/company-news-for-mar-24-2020",
            headers,
        ),
    ],
)
def test_article(spider, response, test_kwargs):
    r = next(spider.parse_article(response=response, **test_kwargs))
    assert r["text"] == (
        "Shares of Hasbro, Inc. HAS jumped 12.5% after the company’s Chief Executive "
        "Officer Brian Goldner reported that supply chains were up and running in "
        "China Shares of PG&E Corporation PCG rose 12.5% after the company announced "
        "that it has entered into a plea agreement and settlement with California to "
        "resolve the criminal prosecution in connection to the 2018 camp fire Shares "
        "of Waitr Holdings Inc. WTRH jumped 27.9% after the company reported "
        "partnership agreement with Ralph's Market to expand into grocery delivery "
        "Shares of AC Immune SA ( ACIU Quick Quote ACIU - Free Report ) rose 13.5% "
        "after the company received a second milestone payment of CHF 10 million from "
        "Eli Lilly"
    )
    assert r["created_at"] == "2020-03-24T00:00:00+00:00"
    assert r["tags"] == ["equity", "zacks", "article", "WTRH"]
    assert r["title"] == "Company News for Mar 24, 2020"
