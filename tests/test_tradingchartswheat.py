"""Test suit for TradingChartsWheat."""

from agblox.spiders.helpers import headers
from agblox.spiders.tradingcharts.wheat import TradingchartswheatSpider
import pytest


@pytest.fixture()
def spider():
    return TradingchartswheatSpider()


headers = headers(TradingchartswheatSpider.host_header)
headers["User-Agent"] = TradingchartswheatSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            TradingchartswheatSpider.url,
            headers,
            [
                "https://futures.tradingcharts.com/news/futures/U_S___Decline_witnessed_in_agricultural_futures_378958904.html",
                "https://futures.tradingcharts.com/news/futures/Feed_Plant_based_Protein_Market_Will_Hit_Big_Revenues_In_Future___Key_Players_are_DuPont__Kerry_Group__Ingredion__Emsland_Group__Kroner__Batory_Foods__Roquette_Freres_378889897.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__Wheat_Protein_Premium_and_Discount_Scales___2021_01_22__usda0z709p94m.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__Daily_Market_Rates__Grain_Miscellaneous_Commodities____2021_01_22__usdawd376p64q.html",
                "https://futures.tradingcharts.com/news/futures/Wheat_Starch_Market_Forecast_to_2027___COVID_19_Impact_and_Global_Analysis_By_Type___Grade_and_End_User_Industry_378419292.html",
                "https://futures.tradingcharts.com/news/futures/55_2__Return_Seen_to_Date_on_SmarTrend_Bunge_Ltd_Call__BG__378395777.html",
                "https://futures.tradingcharts.com/news/futures/Textured_Wheat_Protein_Market_Size__Share_2021_By_Development_History__Business_Prospect__Trend__Key_Manufacturers__Price__Supply_Demand__Growth_Factor_and_End_User_Analysis__Outlook_till_2026_378388879.html",
                "https://futures.tradingcharts.com/news/futures/USDA___AMS__Wheat_Protein_Premium_and_Discount_Scales___2021_01_21__usdakw52k300q.html",
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
            "https://futures.tradingcharts.com/news/futures/USDA___AMS__Bids_for_Grain_Delivered_to_Portland___2018_12_31__usdag445cj59r.html",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["url"]
        == "https://futures.tradingcharts.com/news/futures/USDA___AMS__Bids_for_Grain_Delivered_to_Portland___2018_12_31__usdag445cj59r.html"
    )
    assert (
        r["text"]
        == """USDA U.S. Department of Agriculture - December 31, 2018\nJO_GR110\nPortland, OR Mon Dec 31, 2018 USDA Market News\n***THIS REPORT WILL NOT BE ISSUED TUESDAY JANUARY 1 DUE TO THE HOLIDAY***\nPortland Daily Grain Report\nBids as of 12:00 p.m. Pacific time; Subject to change\nMarch wheat futures trended 1.50 to 8.25 cents per bushel lower compared\nto Friday�s noon closes.\nBids for US 1 Soft White Wheat delivered to Portland in unit trains\nand barges for December delivery ordinary protein trended steady compared\nto Friday�s noon bids for the same delivery period. Some exporters were\nnot issuing bids for nearby delivery. Bids for guaranteed maximum 10.5\npercent protein trended steady compared to Friday�s noon bids for the same\ndelivery period. Some exporters are not issuing bids for nearby delivery.\nBids for 11.5 percent US 1 Hard Red Winter Wheat for December delivery\ntrended 7.25 cents per bushel lower compared to Friday�s noon bids for the\nsame delivery period. Some exporters were not issuing bids for nearby\ndelivery.\nBids for 14 percent protein US 1 Dark Northern Spring Wheat for December\ndelivery trended 1.50 cents per bushel lower compared to Friday�s noon bids\nfor the same delivery period. Some exporters were not issuing bids for\nnearby delivery.\nBids for US 2 Yellow Corn delivered full coast in 110 car shuttle\ntrains for December delivery were not available as most exporters were not\nissuing bids for nearby delivery.\nBids for US 1 Yellow Soybeans delivered full coast in 110 car shuttle\ntrains for December delivery were not available as most exporters were not\nissuing bids for nearby delivery.\nAccording to the Portland Merchant�s Exchange, there were 13 grain\nvessels in Columbia River ports today, with four docked.\nAll bids in dollars per bushel\nUS 1 Soft White Wheat - delivered by Unit Trains and Barges\nOrdinary protein\nDec 6.1500-6.3000 unch\nJan 6.1500-6.3500 dn 3.00-unch\nFeb 6.2100-6.3500 unch\nMar 6.2400-6.3500 unch\nApr 6.2800 dn 2.00-6.00\nGuaranteed maximum 10.5 pct protein\nDec 6.1500-6.3000 unch\nJan 6.1800-6.3500 unch\nFeb 6.2100-6.3500 unch\nMar 6.2400-6.3500 unch\nApr NA\n_\nUS 1 White Club Wheat - delivered by Unit Trains and Barges\nOrdinary protein\nDec 6.1500-6.3000 unch\nGuaranteed maximum 10.5 pct protein\nDec 6.1500-6.3000 unch\n_\nUS 1 Hard Red Winter Wheat - (Exporter bids-falling numbers of 300 or\nbetter)\nOrdinary protein 6.1275-6.3375 dn 7.25\n11 pct protein 6.2675-6.4375 dn 7.25\n11.5 pct protein\nDec 6.3375-6.4875 dn 7.25\nJan 6.3875-6.4875 dn 7.25\nFeb 6.4375-6.4875 dn 7.25\nMar 6.3875-6.4875 dn 7.25\nApr NA\n12 pct protein 6.3375-6.4875 dn 7.25\n13 pct protein 6.3375-6.5875 dn 7.25\n_\nUS 1 Dark Northern Spring Wheat (with a minimum of 300 falling numbers, a maximum\nof 0.5 part per million vomitoxin, and a maximum of one percent total damage)\n13 pct protein 6.3400-6.3600 dn 1.50\n14 pct protein\nDec 6.4400-6.5400 dn 1.50\nJan 6.4400-6.5400 dn 1.50\nFeb 6.4900-6.6700 dn 1.50\nMar 6.5400-6.7000 dn 1.50\nApr NA\n15 pct protein 6.4400-6.5400 dn 1.50\n16 pct protein 6.4400-6.5400 dn 1.50\n_\nUS 2 Yellow Corn\nShuttle trains-Delivered full coast Pacific Northwest-BN\nDec NA\nJan NA\nFeb 4.7600-4.7800 dn 2.50-0.50\nMar 4.7400-4.7500 dn 0.50\nApr 4.7200-4.7500 dn 0.25-up 1.75\nMay 4.7200-4.7500 dn 0.25-up 1.75\n_\nUS 1 Yellow Soybeans\nShuttle trains-Delivered full coast Pacific Northwest-BN\nDec NA\nJan 9.4250-9.4750 dn 0.25-5.25\nFeb 9.6000 dn 0.50-5.50\nMar 9.6000 dn 0.50-5.50\nApr NA\nMay NA\n_\nUS 2 Heavy White Oats ** 3.7750 unch\n** Not well tested.\nExporter Bids Portland Rail/Barge Nov 2018\nAverages in Dollars per bushel\nUS 1 Soft White by Unit Trains and Barges 6.2500\nUS 1 Hard Red Winter (Ordinary protein) 6.1500\nUS 1 Hard Red Winter (11.5% protein) 6.3500\nUS 1 Dark Northern Spring (14% protein) 6.8200\nSource: USDA Market News Service, Portland, OR\nNiki Davila 503-535-5001 Portland.LPGMN@ams.usda.gov\n24 Hour Market Report 503-535-5005\nwww.ams.usda.gov/mnreports/jo_gr110.txt\nwww.ams.usda.gov/lpsmarketnewspage\n11:41P nd"""
    )
    assert r["created_at"] == "2018-12-31T00:00:00+00:00"
    assert r["tags"] == ["wheat", "article", "tradingchartswheat"]
    assert r["title"] == "USDA - AMS: Bids for Grain Delivered to Portland\n(2018-12-31)"
