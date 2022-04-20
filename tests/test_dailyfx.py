"""Test suit for DailyfxSpider."""

from agblox.spiders.dailyfx import DailyfxSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return DailyfxSpider()


headers = headers(DailyfxSpider.host_header)
headers["User-Agent"] = DailyfxSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            DailyfxSpider.url,
            headers,
            [
                "https://www.dailyfx.com/forex/fundamental/us_dollar_index/daily_dollar/2020/11/19/USDCAD-Outlook-Weekly-Range-Remains-Intact-Ahead-of-G20-Summit.html",
                "https://www.dailyfx.com/forex/fundamental/article/special_report/2020/11/19/implied-volatility-what-is-it-and-why-should-traders-care.html",
                "https://www.dailyfx.com/forex/market_alert/2020/11/19/NZDUSD-USD.html",
                "https://www.dailyfx.com/forex/market_alert/2020/11/19/XAUUSD-Forecast-Inflation-and-Excess-Liquidity-to-Keep-Gold-Supported-in-the-Long-Term.html",
                "https://www.dailyfx.com/forex/market_alert/2020/11/19/Bitcoin-BTC-Outlook-Gearing-Up-for-The-Next-Leg-Higher.html",
                "https://www.dailyfx.com/forex/market_alert/2020/11/19/British-Pound-GBP-Latest-GBPUSD-Easing-Ahead-of-EU-Leaders-Summit-MSE.html",
                "https://www.dailyfx.com/forex/fundamental/daily_briefing/session_briefing/euro_open/2020/11/19/SP-500-at-Risk-as-Tightening-Restrictions-Douse-Vaccine-Optimism.html",
                "https://www.dailyfx.com/forex/fundamental/daily_briefing/daily_pieces/commodities/2020/11/19/Crude-Oil-Prices-May-Rise-If-EU-Summit-Stokes-Brexit-Deal-Hopes.html",
                "https://www.dailyfx.com/forex/market_alert/2020/11/19/Nikkei-225-May-Lead-APAC-Stocks-Lower-Virus-Cases-Overshadow-Vaccine-Hopes.html",
                "https://www.dailyfx.com/forex/fundamental/daily_briefing/daily_pieces/asia_am_briefing/2020/11/19/Australian-Dollar-Outlook-AUDUSD-May-Break-Support-on-Jobs-Report.html",
                "https://www.dailyfx.com/forex/market_alert/2020/11/18/canadian-dollar-technical-outlook-usdcad-cadjpy-nzdcad.html",
                "https://www.dailyfx.com/forex/market_alert/2020/11/18/SP-500-Forecast-How-Will-the-Addition-of-Tesla-Impact-the-Index.html",
                "https://www.dailyfx.com/forex/fundamental/us_dollar_index/daily_dollar/2020/11/18/NZDUSD-Rate-Clears-2019-High-and-Triggers-Overbought-RSI-Reading.html",
                "https://www.dailyfx.com/forex/fundamental/us_dollar_index/daily_dollar/2020/11/18/Gold-Prices-to-Watch-as-September-Range-Remains-Intact.html",
                "https://www.dailyfx.com/forex/fundamental/article/special_report/2020/11/18/implied-volatility-what-is-it-and-why-should-traders-care.html",
                "https://www.dailyfx.com/forex/market_alert/2020/11/18/EURUSD-EURGBP.html",
                "https://www.dailyfx.com/forex/market_alert/2020/11/18/CAC-40-Forecast-Ready-to-Overcome-Key-Fibonacci-Resistance-.html",
                "https://www.dailyfx.com/forex/market_alert/2020/11/19/CAC-40-Forecast-Ready-to-Overcome-Key-Fibonacci-Resistance-.html",
                "https://www.dailyfx.com/forex/market_alert/2020/11/18/US-Dollar-Sell-Off-Continues-USDJPY-Falls-Back-Below-104.00.html",
                "https://www.dailyfx.com/forex/market_alert/2020/11/18/British-Pound-GBP-Latest-GBPUSD-Trend-Higher-May-Persist-After-UK-Inflation-Data-MSE.html",
                "https://www.dailyfx.com/market-news/articles/2",
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
            "https://www.dailyfx.com/market-news/articles/1482",
            headers,
            [
                "https://www.dailyfx.com/forex/fundamental/us_dollar_index/daily_dollar/2012/01/03/USD_Index_Searches_For_Support_Euro_Threatens_Downward_Trend.html",
                "https://www.dailyfx.com/forex/fundamental/article/weekly_strategy_outlook/2012/01/03/forex_strategy_trading_outlook_new_year.html",
                "https://www.dailyfx.com/forex/fundamental/daily_briefing/session_briefing/us_open/2012/01/03/USD_Struggles_Ahead_Of_FOMC_Minutes_Euro_Weakness_Ahead.html",
                "https://www.dailyfx.com/forex/fundamental/daily_briefing/daily_pieces/commodities/2012/01/03/Crude_Oil_Poised_to_Follow_Stocks_Higher_Gold_Eyes_FOMC_Minutes.html",
                "https://www.dailyfx.com/forex/fundamental/article/fundamental_trends_monitor/2012/01/03/Dollar_Faces_Tough_Week_Ahead_as_Focus_Turns_to_US_Economic_Data.html",
                "https://www.dailyfx.com/forex/fundamental/daily_briefing/session_briefing/euro_open/2012/01/03/FOREX_US_Dollar_Under_Pressure_as_Stocks_Drive_Higher_to_Start_2012.html",
                "https://www.dailyfx.com/forex/fundamental/daily_briefing/daily_pieces/opening_comment/2012/01/03/Early_2012_Price_Action_is_Risk_Positive_but_Will_it_Last.html",
                "https://www.dailyfx.com/forex/fundamental/daily_briefing/daily_pieces/opening_comment/2012/01/02/Monday_Trading_Conditions_Expected_to_be_Very_Thin_China_PMIs_Solid.html",
                "https://www.dailyfx.com/forex/market_alert/2012/01/10/011012_Canada_Housing_Starts_December.html",
                "https://www.dailyfx.com/forex/fundamental/daily_briefing/session_briefing/euro_open/2020/06/05/AUDUSD-and-USDJPY-Rally-Ahead-Of-US-NFP-Report.html",
                "https://www.dailyfx.com/forex/fundamental/forecast/weekly/chf/2012/06/09/Gold_Posts_Largest_Loss_in_4_Weeks_as_Bernanke_Quiets_QE_Speculation.html",
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
            "https://www.dailyfx.com/forex/analyst_picks/todays_picks/michael_boutros/2020/11/19/US-Dollar-Technical-Price-Setups-EUR-USD-AUD-MXN-Trade-Forecast-MBTS11.html",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Near-term Technical Outlook: Trade Setups on EUR/USD, AUD/USD & USD/MXN "
        "Technical charts on trade setup we’ve been tracking in , & weekly "
        "opening-range set below key resistance Aussie fails third attempt to breach "
        "late-September highs /MXN inflection risk as sell-off tests critical support "
        "zone Advertisement An update on technical setups we' v e been tracking in "
        "Euro, Aussie & Peso. These are the targets and invalidation levels that "
        "matter heading into the close of the week . Review my latest Strategy "
        "Webinar for an in-depth breakdown of these trade setup s and more. Euro "
        "Price Chart – EUR/USD 120min Chart Prepared by Michael Boutros , Technical "
        "Strategist; EUR/USD on Tradingview In last week’s Euro Price Outlook we "
        "noted that, “ the threat remains for a deeper pullback while below the "
        "weekly open at 1.1890 – look for topside exhaustion ahead of this threshold "
        "IF price is heading lower .” Euro registered a low at 1.1745 in the "
        "following days before rebounding with price once again carving a weekly "
        "opening-range just below key resistance at 1.1911/23 . Bottom line: Risk for "
        "further losses while below this threshold - initial support at the weekly "
        "range lows at 1.1814 with a break lower exposing 1.1761 and the 61.8% "
        "Fibonacci retracement of the November range at 1.1723 – look for a larger "
        "reaction there for guidance IF reached. A topside breach / close above "
        "1.1924 is needed to mark resumption towards subsequent resistance objectives "
        "at 1.1961 and the upper parallel / 2018 yearly open at 1.2005 . Review my "
        "latest Euro Weekly Price Outlook for a look at the longer-term EUR/USD "
        "technical trade levels. Australian Dollar Price Chart - AUD/USD 120min Chart "
        "Prepared by Michael Boutros , Technical Strategist; AUD/USD on Tradingview "
        "In my most recent Australian Dollar Technical Price Outlook we noted that "
        "/USD was trading into a key resistance zone and to , “be on the lookout for "
        "possible topside exhaustion with the immediate advance vulnerable while "
        "below the September high-day close.” The setup remains unchanged into the "
        "close of the week with Aussie attempting to break the weekly opening-range "
        "lows today. Bottom line: Initial resistance steady at 7321/29 with the "
        "threat of topside exhaustion sub- 7371 . A break below the median-line here "
        "is needed to suggest a larger correction is underway towards 7222 , 7166 and "
        "the 61.8% retracement at 7125 - look for a larger reaction there IF reached. "
        "Review my latest Aussie Weekly Price Outlook for a look at the longer-term "
        "AUD/USD technical trade levels. Australian Dollar Trader Sentiment – AUD/USD "
        "Price Chart A summary of IG Client Sentiment shows traders are net-short "
        "AUD/USD - the ratio stands at -2.04 (32.89% of traders are long) – bullish "
        "reading Long positions are 0.67% lower than yesterday and 10.31% higher from "
        "last week Short positions are 2.90% lower than yesterday and 3.40% lower "
        "from last week We typically take a contrarian view to crowd sentiment, and "
        "the fact traders are net-short suggests AUD/USD prices may continue to rise. "
        "Yet traders are less net-short than yesterday and compared with last week. "
        "Recent changes in sentiment warn that the current AUD/USD price trend may "
        "soon reverse lower despite the fact traders remain net-short. AUD/USD "
        "BEARISH Data provided by\nof clients are net long.\n"
        "of clients are net short. Mexican Peso Price Chart – USD/MXN Daily Chart "
        "Prepared by Michael Boutros , Technical Strategist; USD/MXN on Tradingview "
        "In this month’s Mexican Peso Price Outlook we noted that USD/MXN that a "
        "weekly reversal had shifted the focus lower in price, “ keeping the focus on "
        "the 2019 swing high at 20.2561 and the 78.6% Fibonacci retracement at "
        "20.0752 . ” Price registered a low at 20.0329 last week before rebounding "
        "with USD/MXN once again approaching the 2019 high-day close / Fibonacci "
        "support at 20.0752/1360 – looking for inflection off this threshold. Bottom "
        "line: USD/MXN is poised to mark an outside-day reversal lower today but keep "
        "price above key s upport . A good zone to reduce short-exposure / lower "
        "protective stops – a break / close below 20.0752 is needed to keep the "
        "short-bias viable towards 19.8794 and 19.6591 . Initial resistance stands at "
        "last week’s high / the 75% parallel at ~ 20.6930 with a break above 20.8377 "
        "needed to shift the focus higher in USD/MXN. For a complete breakdown of "
        "Michael’s trading strategy, review his Foundations of Technical Analysis "
        "series on B uilding a T rading S trategy -Written by Michael Boutros , "
        "Currency Strategist with DailyFX Follow Michael on Twitter @MBForex"
    )
    assert r["created_at"] == "2020-11-19T17:49:00+00:00"
    assert r["tags"] == ["forex", "article", "dailyfx"]
    assert r["title"] == "US Dollar Technical Price Setups: EUR/USD, AUD/USD & USD/MXN"
