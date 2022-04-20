"""Test suit for BabyPips."""

from agblox.spiders.babypips import BabyPipsSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return BabyPipsSpider()


headers_dict = headers(BabyPipsSpider.host_header)
headers_dict["User-Agent"] = BabyPipsSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            BabyPipsSpider.url,
            headers_dict,
            [
                "https://www.babypips.com/news/daily-us-watchlist-20210113",
                "https://www.babypips.com/news/daily-london-watchlist-20210113",
                "https://www.babypips.com/news/daily-us-watchlist-20210112",
                "https://www.babypips.com/news/covid-19-pandemic-vaccine-race-2021",
                "https://www.babypips.com/news/daily-london-watchlist-20210112",
                "https://www.babypips.com/news/daily-us-watchlist-20210111",
                "https://www.babypips.com/news/forex-market-outlook-210111",
                "https://www.babypips.com/news/usd-weekly-forecast-20210111",
                "https://www.babypips.com/news/cad-weekly-forecast-20210111",
                "https://www.babypips.com/news/gbp-weekly-forecast-mid-tier-data-mpc-speeches-lined",
                "https://www.babypips.com/news/eur-chf-weekly-forecast-20210111",
                "https://www.babypips.com/news/jpy-weekly-forecast-20210111",
                "https://www.babypips.com/news/aud-weekly-forecast-20210111",
                "https://www.babypips.com/news/nzd-weekly-forecast-20210111",
                "https://www.babypips.com/news/forex-mechanical-systems-20210108",
                "https://www.babypips.com/news/usd-weekly-review-20210108",
                "https://www.babypips.com/news/gbp-weekly-review-20210108",
                "https://www.babypips.com/news/eur-chf-weekly-review-20210108",
                "https://www.babypips.com/news/cad-weekly-review-20210108",
                "https://www.babypips.com/news/nzd-weekly-review-20210108",
                "https://www.babypips.com/news/2",
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
            "https://www.babypips.com/news/693",
            headers_dict,
            [
                "https://www.babypips.com/news/how_many_employees_does_it_take",
                "https://www.babypips.com/news/the_correlation_between_the_an",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 2
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.babypips.com/news/almost-80-percent-of-retail-traders-are-unprofitable",
            headers_dict,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Trading is hard . So hard that recent data disclosed by trading platforms "
        "show that, on average, less than 1 out of 4 retail traders make money . "
        "Outside of the U.S., forex is commonly traded by retail traders using "
        "Contract for Differences (CFDs). If you’re not familiar with CFDs, a CFD is "
        "a contract entered between a trader and a CFD provider. CFDs allow traders "
        "to speculate on rising or falling prices in an underlying currency pair "
        "(along with other underlying markets like indices, shares, commodities, and "
        "crypto). Due to the recent measures adopted by the European Securities and "
        "Markets Authority (ESMA), companies that offer CFDs to retail clients are "
        "now required to display a “ standardised risk warning, including the "
        "percentage of losses on a CFD provider’s retail investor accounts. ” "
        "Basically, trading platforms are forced to be more TRANSPARENT and now have "
        "to disclose what percentage of their clients are losing money . At the "
        "bottom of each CFD provider’s website, they display a message that looks "
        "something like this: Please note that CFDs are complex instruments and come "
        "with a high risk of losing money rapidly due to leverage. X% of retail "
        "investor accounts lose money when trading CFDs with this provider. You "
        "should consider whether you understand how CFDs work, and whether you can "
        "afford to take the high risk of losing your money. Here’s an actual example: "
        "I was curious to know what the numbers were across different CFD providers. "
        "To be clear, the number displayed consists of ALL types of CFDs traded, not "
        "just forex , but I thought it would still give a pretty good idea of how "
        "retail traders fare in general. I looked at the websites of 28 of the most "
        "popular CFD providers and discovered that the percentage of losing accounts "
        "ranged between 54% and 83%, with the average being 76% in the red. That "
        "means less than 1 out of 4 traders make money. Here’s a chart showing just "
        "the percentage of losing accounts for each specific CFD provider. In an "
        "attempt to temporarily blind you with bright colors, the charts below breaks "
        "down the actual percentages between winning and losing retail accounts for "
        "each CFD provider. This chart displays CFD providers in alphabetical order . "
        "This chart below sorts CFD providers who have the highest percentage of "
        "winning retail accounts to the lowest. I’m not trying to pick on a specific "
        "trading platform here. It’s not necessarily their fault that their clients "
        "are losing money. My point in showing this data is to emphasize that is "
        "trading is NOT easy. The data shows that it is NORMAL for 70-80% of traders "
        "to be unprofitable. Said differently, out of every 10 traders, only 2-3 "
        "traders succeed ! If you’re a new trader, I’m not trying to discourage you. "
        "But here at BabyPips.com, we want to make sure your expectations are "
        "realistic . Don’t be fooled by the “forex traders” posting videos of "
        "themselves chillin’ in their Versace furnished luxury penthouse suites, "
        "driving their Lamborghini Huracán, while flossin’ their Rolex Submariner and "
        "rockin’ Gucci slides. That said, check out my ride. I started trading micro "
        "lots and now look at what I drive! All because of forex trading! If I can do "
        "it, so can you! Yeah right. I don’t own this car. Were you not paying any "
        "attention to what I just said… It is not easy to make money trading forex. "
        "Or stocks. Or crypto. Or commodities. Or indices. Or bonds. Or . Forex "
        "trading is not a get-rich-quick scheme . Trading is a skill that takes TIME "
        "to learn. Learning and applying risk management concepts such as proper "
        "position sizing and understanding leverage is also crucial. We emphasize "
        "these points repeatedly in our School of Pipsology . If you were thinking "
        "about getting rich quick through trading, this data should make you think "
        "twice! If it makes you feel any better, becoming a professional basketball "
        "player is even harder . For men, about three out of 10,000 male high school "
        "basketball players will be drafted into the NBA, or about .03 percent . For "
        "women, around one out of 5,000 players, or .02 percent , will be drafted "
        "into the WNBA. Did you know that the five deadliest factors that cause "
        "traders to fail are self-inflicted? Learn about the 5 Things That Traders Do "
        "to Guarantee Their Own Failure . If you’re interested in seeing the raw data "
        "in table form, enjoy! *Data from 01/31/2019 so current numbers could be "
        "different."
    )
    assert r["created_at"] == "2019-02-09T15:30:53Z"
    assert r["tags"] == ["Forex", "article", "babypips.com"]
    assert r["title"] == "Data Confirms Grim Truth: 70-80% of Retail Traders are Unprofitable"
