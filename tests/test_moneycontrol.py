"""Test suit for MoneyControlSoy."""

from agblox.spiders.helpers import headers
from agblox.spiders.moneycontrol import MoneycontrolSpider
import pytest


@pytest.fixture()
def spider():
    return MoneycontrolSpider()


headers = headers(MoneycontrolSpider.host_header)
headers["User-Agent"] = MoneycontrolSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            MoneycontrolSpider.url,
            headers,
            [
                "https://www.moneycontrol.com/news/business/economy/excessive-rains-pest-attack-trims-indian-soybean-crop-trade-body-5953991.html",
                "https://www.moneycontrol.com/news/business/commodities/soybean-futures-dip-marginally-to-rs-3886-37-per-quintal-on-weak-demand-5848151.html",
                "https://www.moneycontrol.com/news/india/forecasts-of-heavy-rains-raise-fear-for-summer-crops-in-india-5844141.html",
                "https://www.moneycontrol.com/news/business/commodities/super-trend-gives-sell-signal-initiates-short-position-in-mcx-soybean-september-future-5709381.html",
                "https://www.moneycontrol.com/news/business/commodities/soybean-futures-rise-on-fresh-bets-5348921.html",
                "https://www.moneycontrol.com/news/business/commodities/soybean-futures-slip-on-muted-demand-4-5298221.html",
                "https://www.moneycontrol.com/news/business/commodities/soybean-futures-slip-on-muted-demand-3-5292801.html",
                "https://www.moneycontrol.com/news/business/commodities/soybean-futures-slip-on-muted-demand-2-5287441.html",
                "https://www.moneycontrol.com/news/business/soybean-futures-slip-on-muted-demand-5255501.html",
                "https://www.moneycontrol.com/news/business/commodities/buy-ncdex-april-soybean-at-rs-3880quintal-for-target-rs-4200-choice-broking-5091691.html",
                "https://www.moneycontrol.com/news/business/stocks/soybean-prices-are-expected-to-trade-sideways-today-angel-commodities-9-4356421.html",
                "https://www.moneycontrol.com/news/business/stocks/soybean-prices-to-trade-sideways-to-lower-angel-commodities-16-4301441.html",
                "https://www.moneycontrol.com/news/trade-2/indias-july-soymeal-exports-plunge-59-yoy-to-near-three-year-low-trade-body-4296611.html",
                "https://www.moneycontrol.com/news/business/stocks/soybean-prices-to-trade-sideways-to-lower-angel-commodities-15-4289891.html",
                "https://www.moneycontrol.com/news/business/stocks/soybean-prices-to-trade-sideways-to-lower-angel-commodities-14-4270121.html",
                "https://www.moneycontrol.com/news/business/stocks/soybean-prices-to-trade-sideways-to-positive-angel-commodities-4249751.html",
                "https://www.moneycontrol.com/news/business/stocks/soybean-prices-are-expected-to-trade-sideways-today-angel-commodities-8-4213291.html",
                "https://www.moneycontrol.com/news/business/stocks/soybean-prices-are-expected-to-trade-sideways-today-angel-commodities-7-4197681.html",
                "https://www.moneycontrol.com/news/business/stocks/soybean-prices-are-expected-to-trade-sideways-today-angel-commodities-6-4168271.html",
                "https://www.moneycontrol.com/news/world/igc-cuts-forecasts-for-201920-world-corn-soy-crops-4146391.html",
                "https://www.moneycontrol.com/news/business/stocks/soybean-prices-are-expected-to-trade-sideways-today-angel-commodities-5-4138591.html",
                "https://www.moneycontrol.com/news/business/markets/bearish-price-outlook-soybean-4118661.html",
                "https://www.moneycontrol.com/news/business/stocks/soybean-prices-are-expected-to-trade-sideways-today-angel-commodities-4-4109271.html",
                "https://www.moneycontrol.com/news/business/stocks/soybean-prices-to-trade-sideways-to-lower-angel-commodities-13-4062031.html",
                "https://www.moneycontrol.com/news/business/stocks/soybean-futures-expected-to-trade-sideways-angel-commodities-5-4042041.html",
                "https://www.moneycontrol.com/news/tags/soybean.html/page-2/",
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
            "https://www.moneycontrol.com/news/tags/soybean.html/page-25/",
            headers,
            [
                "https://www.moneycontrol.com/news/trends/current-affairs-trends/-2117335.html",
                "https://www.moneycontrol.com/news/trends/features-2/-1240929.html",
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
            "https://www.moneycontrol.com/news/business/commodities/buy-ncdex-april-soybean-at-rs-3880quintal-for-target-rs-4200-choice-broking-5091691.html",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))

    assert (
        r["url"]
        == "https://www.moneycontrol.com/news/business/commodities/buy-ncdex-april-soybean-at-rs-3880quintal-for-target-rs-4200-choice-broking-5091691.html"
    )

    assert (
        r["text"]
        == """NCDEX Soybean spot price has been trading bearish during the month of March so far closing at Rs.3701/quintal by 27 March. It is lower by 4.37 percent compared to Rs. 3870/quintal reported on 2 March. Weak export buying in the global markets especially from China due to the outbreak of Coronavirus led to panic selling the Indore Soybean prices. On the other hand, NCDEX Soybean April Futures closed at Rs.3812/quintal on 27th March, higher compared to Rs.3632/quintal reported on 2 March. Futures prices witnessed faster discounting and later fresh buying was observed at lower levels which led to upside movement in the same period. Fundamentally for the month ahead, NCDEX Soybean futures is estimated to remain bullish due to higher demand for groceries in the domestic market. In the current lockdown scenario, no new arrivals by the farmers have been reported in the APMC market of Indore, and traders are releasing their old stocks to satisfy the local wholesale and retail demand. Due to delayed interstate and inter district level transportation for essential commodities, traders continue to buy Soybean in the futures market amid fears of supply tightness in the coming weeks. Moreover, the recent stimulus package of $2 trillion by the United States could prove to be beneficial for the US farmers and eventually support the CBOT Soybean prices. Furthermore, lockdown and rising deaths in the United States could affect sowing in the United States and the market is fearing for global supply tightness. Recent news has reported that United states could possibly be under lockdown till 30 April which is also expected to support Soybean prices in the weeks ahead. Soybean sowing in United States could be delayed amid lockdown situation, however, the demand for Soymeal has substantially declined globally due to COVID-19 which is expected to cap major upside movement in the coming weeks. Overall, we expect a bullish trend for the month ahead and recommend buying in NCDEX Soybean April Futures at CMP Rs.3880/quintal for a target price of Rs.4200/quintal and maintaining a stop loss below Rs.3720/quintal."""
    )

    assert r["created_at"] == "2020-03-31T03:24:39+05:30"
    assert r["tags"] == ["article", "moneycontrol.com"]
    assert (
        r["title"]
        == "Buy NCDEX April Soybean At Rs 3,880/Quintal For Target Rs 4,200: Choice Broking"
    )
