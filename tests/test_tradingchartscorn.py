"""Test suit for SoybeansandcornSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.tradingcharts.corn import TradingchartscornSpider
import pytest


@pytest.fixture()
def spider():
    return TradingchartscornSpider()


headers = headers(TradingchartscornSpider.host_header)
headers["User-Agent"] = TradingchartscornSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            TradingchartscornSpider.url,
            headers,
            [
                "https://futures.tradingcharts.com/news/futures/A_New_Brand_for_Kitchenwares__They_Are_Trying_to_Share_Their_Cooking_Experience_with_New_Angle_374300846.html",
                "https://futures.tradingcharts.com/news/futures/Roasted_Corn_Market_Technologies__Sales_Revenue__Key_Players_Analysis__Development_Status_and_Industry_Expansion_Strategies_2027_374280325.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__South_Carolina_Farmers_Market___Columbia__SC___2020_11_10__usdagb19fx94m.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__Weekly_Shipments__Movement____Corn___2020_11_10__usda9s161x423.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__Weekly_Shipment__Movement__Report__Fruit_and_Vegetables___2020_11_10__usdajq0869396.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__Daily_Market_Rates__Grain_Miscellaneous_Commodities____2020_11_10__usda8p58q412h.html",
                "https://futures.tradingcharts.com/news/futures/Green_Plains_to_Present_at_Stephens_Annual_Investment_Conference_374190750.html",
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
            "https://futures.tradingcharts.com/news/futures/USDA___AMS__Kansas_City_Grain_Prices_Spot_FOB_Rail___2019_01_11__usda6h440z46m.html",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        """USDA U.S. Department of Agriculture - January 11, 2019\nSJ_GR110\nSt. Joseph, MO Fri, Jan 11, 2019 USDA-MO Dept of Ag Market News\nKansas City Daily Wheat Bids, FOB Track, dollars per bushel\nFutures (Mar) 5.0450\nChange (�/bu) Basis Change\nHRW Wheat:\nOrd Protein 6.1450-6.2950 UP 5.75 110H to 125H UNCH\n11.00 Pct Prot. 6.2450-6.3950 UP 5.75 120H to 135H UNCH\n11.20 Pct Prot. 6.2450-6.3950 UP 5.75 120H to 135H UNCH\n11.40 Pct Prot. 6.2450-6.3950 UP 5.75 120H to 135H UNCH\n11.60 Pct Prot. 6.2450-6.3950 UP 5.75 120H to 135H UNCH\n11.80 Pct Prot. 6.2450-6.3950 UP 5.75 120H to 135H UNCH\n12.00 Pct Prot. 6.2450-6.3950 UP 5.75 120H to 135H UNCH\n12.20 Pct Prot. 6.2450-6.3950 UP 5.75 120H to 135H UNCH\n12.40 Pct Prot. 6.2950-6.4450 UP 5.75 125H to 140H UNCH\n12.60 Pct Prot. 6.2950-6.4450 UP 5.75 125H to 140H UNCH\n12.80 Pct Prot. 6.2950-6.4450 UP 5.75 125H to 140H UNCH\n13.00 Pct Prot. 6.2950-6.4450 UP 5.75 125H to 140H UNCH\n13.20 Pct Prot. 6.2950-6.4450 UP 5.75 125H to 140H UNCH\n13.40 Pct Prot. 6.2950-6.4450 UP 5.75 125H to 140H UNCH\n13.60 Pct Prot. 6.2950-6.4450 UP 5.75 125H to 140H UNCH\n13.80 Pct Prot. 6.2950-6.4450 UP 5.75 125H to 140H UNCH\n14.00 Pct Prot. 6.2950-6.4450 UP 5.75 125H to 140H UNCH\nSRW Wheat NQ NQ NQ NQ\nWhite Corn 3.9175-3.9425 UP 0.75-DN 3.5\nCash bids reflect the difference between the basis and the futures settlement.\nHRW Wheat = US 1; SRW Wheat = US 2; White Corn = US 2\nKansas City Board of Trade symbols: F January, G February, H March, J April,\nK May, M June, N July, Q August, U September, V October, X November, Z December\n----------------------------------------------------------------------------------\nMonthly Prices for: December 2018\nHRW Wheat (Ord Protein) 6.3578\n(13 Pct Protein) 6.5814\nSRW Wheat NA\nWhite Corn 3.8167\nSource: USDA Livestock, Poultry and Grain Market News Division, St. Joseph, MO\nVoluntary Staff 816-676-7000 StJoe.LPGMN@usda.gov\nwww.ams.usda.gov/mnreports/SJ_GR110.txt\nwww.ams.usda.gov/LPSMarketNewsPage\n1336 C"""
    )
    # created at not checked as cannot reliably extract date
    assert r["tags"] == ["corn", "article", "tradingchartscorn"]
    assert r["title"] == "USDA - AMS: Kansas City Grain Prices Spot FOB Rail\n(2019-01-11)"
