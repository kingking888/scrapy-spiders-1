"""Test suit for SoybeansandcornSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.tradingcharts.soy import TradingchartssoySpider
import pytest


@pytest.fixture()
def spider():
    return TradingchartssoySpider()


headers = headers(TradingchartssoySpider.host_header)
headers["User-Agent"] = TradingchartssoySpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            TradingchartssoySpider.url,
            headers,
            [
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__Daily_Market_Rates__Grain_Miscellaneous_Commodities____2020_11_12__usdacv43pn49r.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__Daily_Market_Rates__Grain_Miscellaneous_Commodities____2020_11_10__usda8p58q412h.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__Daily_Market_Rates__Grain_Miscellaneous_Commodities____2020_11_09__usdacz30qj244.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__Daily_Market_Rates__Grain_Miscellaneous_Commodities____2020_11_06__usdatt44qc54n.html",
                "https://futures.tradingcharts.com/news/futures/After_potato___onion__edible_oil_burns_hole_in_pockets_374022194.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__Daily_Market_Rates__Grain_Miscellaneous_Commodities____2020_11_05__usda4t64hb87g.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__National_Feedstuffs_Market_Review___2020_11_04__usda2514p9592.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__Daily_Market_Rates__Grain_Miscellaneous_Commodities____2020_11_04__usdaw3763z29x.html",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    # the website is very long (50+ articles), would be impractical to put all of them in test
    assert r[: len(expected)] == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://futures.tradingcharts.com/news/futures/USDA___AMS__Alabama_Weekly_Feedstuff_Production_Cost_Report__Mon____2019_01_07__usdah415pf894.html",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["url"]
        == "https://futures.tradingcharts.com/news/futures/USDA___AMS__Alabama_Weekly_Feedstuff_Production_Cost_Report__Mon____2019_01_07__usdah415pf894.html"
    )
    assert (
        r["text"]
        == """USDA U.S. Department of Agriculture - January 7, 2019\nMG_GR210\nMontgomery, AL Mon January 07, 2019 USDA-AL Dept of Ag Market News\nAlabama Weekly Feedstuff/Production Cost Report\nFeedstuff prices, dollars per ton, bulk, truck delivered to areas\nin state unless otherwise stated.\nCompared to two weeks ago: Whole cottonseed and gin trash steady,\nsoy hull pellets mostly 5.00 to 40.00 higher, corn gluten pellets\nsteady to 5.00 lower, corn mostly steady, fertilizer and lime steady,\nfarm diesel steady to mostly .09 lower.\nWhole Cottonseed (FOB Gin) 145.00-165.00 Gin Trash 12.00-15.00\nNorth Central South\nSoybean Hull Pellets 160.00-175.00 185.00-250.00 195.00-250.00\nCorn Gluten Pellets 21% prot 160.00-250.00 180.00-265.00 200.00-280.00\n# 2 yellow Corn per bushel 3.85-4.37 3.85-4.57 3.85-4.70\n(rounded to nearest whole cent)\nProduction cost items state wide: cash prices bulk, FOB distributor,\nPer ton unless otherwise stated. Fertilizer in granular form unless\nnoted.\nLiquid Nitrogen 28% spread 300.00-390.00\nAmmonium Nitrate 355.00-425.00\nUrea 350.00-490.00\n13-13-13 (lbs N-P-K per 100 lbs fert) 365.00-425.00\n17-17-17 (lbs N-P-K per 100 lbs fert) 429.00-490.00\nDAP (Diammonium Phosphate 18%N 46%P) 441.00-626.00\nLime (spread) 30.00-50.00\nPotash (Potassium) 320.00-455.00\nFarm Diesel Fuel per gal <1000 gallons 2.01-2.84\nSource: USDA-AL Dept of Ag Market News, Montgomery, AL\nDavid Garcia, OIC\nJohnny Young, Market Reporter Phone 334-223-7488\nwww.ams.usda.gov/mnreports/MG_GR210.txt\n940cst jy vm"""
    )
    assert r["created_at"] == "2019-01-07T00:00:00+00:00"
    assert r["tags"] == ["soy", "article", "tradingchartssoy"]
    assert (
        r["title"]
        == "USDA - AMS: Alabama Weekly Feedstuff/Production Cost Report (Mon)\n(2019-01-07)"
    )
