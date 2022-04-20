"""Test suit for investopedia."""

from agblox.spiders.helpers import headers
from agblox.spiders.investopedia import InvestopediaCompanyNewsSpider
import pytest


@pytest.fixture()
def spider():
    return InvestopediaCompanyNewsSpider()


headers_dict = headers(InvestopediaCompanyNewsSpider.host_header)
headers_dict["User-Agent"] = InvestopediaCompanyNewsSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            InvestopediaCompanyNewsSpider.url,
            headers_dict,
            [
                "https://www.investopedia.com/solar-stocks-enter-secular-uptrend-5092976",
                "https://www.investopedia.com/retail-stocks-could-sell-off-in-coming-weeks-5092966",
                "https://www.investopedia.com/homebuilder-stocks-gain-on-increasing-housing-activity-5092949",
                "https://www.investopedia.com/microsoft-msft-removed-malware-from-solarwinds-swi-hack-5092938",
                "https://www.investopedia.com/crypto-exchange-coinbase-files-for-an-ipo-5092868",
                "https://www.investopedia.com/automatic-data-processing-adp-could-hit-all-time-high-5092867",
                "https://www.investopedia.com/5-companies-owned-by-nvda-5092734",
                "https://www.investopedia.com/5-companies-owned-by-v-5092757",
                "https://www.investopedia.com/3-companies-owned-by-lmt-5092663",
                "https://www.investopedia.com/companies-owned-by-tesla-5092764",
                "https://www.investopedia.com/companies-owned-by-micron-5092627",
                "https://www.investopedia.com/companies-owned-by-square-5092655",
                "https://www.investopedia.com/drive-shack-ds-sees-golden-cross-5092790",
                "https://www.investopedia.com/hp-hpq-rallies-to-a-2-year-high-5092733",
                "https://www.investopedia.com/sec-fines-robinhood-for-misleading-customers-5092776",
                "https://www.investopedia.com/companies-owned-by-jpmorgan-chase-and-co-5092490",
                "https://www.investopedia.com/companies-owned-by-ibm-5092453",
                "https://www.investopedia.com/how-solarwinds-makes-money-5092559",
                "https://www.investopedia.com/states-sue-google-for-antitrust-violations-5092644",
                "https://www.investopedia.com/chart-patterns-suggest-value-stocks-are-headed-higher-5092576",
                "https://www.investopedia.com/apple-aapl-offers-privacy-nutrition-labels-in-app-store-5092537",
                "https://www.investopedia.com/microsoft-msft-announces-safe-gaming-partnership-5092533",
                "https://www.investopedia.com/the-biggest-stock-surprises-of-2020-5092519",
                "https://www.investopedia.com/twitter-twtr-gains-as-jpmorgan-calls-it-a-top-pick-5092546",
                "https://www.investopedia.com/chipotle-mexican-grill-cmg-could-break-out-into-2021-5092543",
                "https://www.investopedia.com/blackberry-bb-may-have-entered-new-uptrend-5092532",
                "https://www.investopedia.com/home-furnishing-stocks-trade-near-floor-of-support-5092512",
                "https://www.investopedia.com/lululemon-lulu-poised-to-maintain-momentum-5092478",
                "https://www.investopedia.com/aphria-and-tilray-combine-to-create-world-s-biggest-cannabis-company-5092540",
                "https://www.investopedia.com/giving-thanks-for-u-s-cannabis-5092399",
                "https://www.investopedia.com/articles/insights/052616/top-4-tesla-shareholders-tsla.asp",
                "https://www.investopedia.com/telecom-stocks-charts-suggest-strength-in-2021-5092395",
                "https://www.investopedia.com/apple-aapl-iphone-subcontractor-rocked-by-worker-riot-5092354",
                "https://www.investopedia.com/carvana-cvna-could-extend-rally-on-bullish-initiation-5092363",
                "https://www.investopedia.com/peloton-pton-could-lose-ground-in-coming-weeks-5092352",
                "https://www.investopedia.com/roku-roku-could-hit-500-in-2021-5092344",
                "https://www.investopedia.com/nike-q2-2021-earnings-5092018",
                "https://www.investopedia.com/disney-dis-retreats-from-record-highs-5092168",
                "https://www.investopedia.com/nike-nke-firing-on-all-cylinders-ahead-of-report-5092158",
                "https://www.investopedia.com/fedex-fdx-testing-2018-resistance-ahead-of-earnings-5092150",
                "https://www.investopedia.com/food-and-beverage-stocks-wrapping-up-a-bad-year-5091916",
                "https://www.investopedia.com/broadcom-avgo-selling-off-despite-strong-quarter-5091900",
                "https://www.investopedia.com/disney-dis-investor-day-2020-highlights-5091877",
                "https://www.investopedia.com/airbnb-adds-heat-to-the-ipo-boom-5091845",
                "https://www.investopedia.com/levi-strauss-jumps-after-goldman-sachs-upgrade-5091729",
                "https://www.investopedia.com/facebook-risks-losing-its-drivers-of-growth-in-antitrust-lawsuits-5091668",
                "https://www.investopedia.com/doordash-dash-opening-print-could-offer-profitable-trade-5091657",
                "https://www.investopedia.com/roku-roku-jumps-after-analysts-cite-2021-potential-5090715",
                "https://www.investopedia.com/starbucks-names-mellody-hobson-non-executive-chairman-5090718",
                "https://www.investopedia.com/is-it-time-to-buy-intel-intc-5090673",
                "https://www.investopedia.com/microsoft-makes-azure-digital-twins-generally-available-5090654",
                "https://www.investopedia.com/us-steel-x-doubles-in-price-in-just-6-weeks-5090668",
                "https://www.investopedia.com/2-hospital-stocks-set-to-benefit-beyond-the-pandemic-5090659",
                "https://www.investopedia.com/betterment-co-founder-jonathan-stein-steps-down-as-ceo-5090524",
                "https://www.investopedia.com/exxonmobil-targeted-by-activist-investor-seeking-board-changes-5090505",
                "https://www.investopedia.com/global-infrastructure-investments-poised-for-2021-gains-5090476",
                "https://www.investopedia.com/on-semiconductor-on-extends-rally-on-ceo-appointment-5090463",
                "https://www.investopedia.com/apple-aapl-announces-airpods-max-5090447",
                "https://www.investopedia.com/adobe-adbe-perfectly-positioned-for-new-highs-5090448",
                "https://www.investopedia.com/toll-brothers-tol-earnings-bode-well-for-homebuilders-5090446",
                "https://www.investopedia.com/cree-cree-consolidates-after-morgan-stanley-downgrade-5090365",
                "https://www.investopedia.com/costco-cost-at-technical-crossroads-ahead-of-earnings-5090276",
                "https://www.investopedia.com/apple-aapl-sees-increased-complaints-about-iphone-12-5090203",
                "https://www.investopedia.com/lower-jinkosolar-jks-guidance-pressures-solar-stocks-5090269",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.investopedia.com/2-hospital-stocks-set-to-benefit-beyond-the-pandemic-5090659",
            headers_dict,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))

    assert (
        r["url"]
        == "https://www.investopedia.com/2-hospital-stocks-set-to-benefit-beyond-the-pandemic-5090659"
    )

    assert r["text"] == (
        "Hospital stocks trail the S&P 500 by around 15% since the start of the year as plunging "
        "non-emergency admissions brought about by the pandemic have weighed heavily on industry "
        "profits. Despite voluntary hospital visitations likely to remain low amid rising "
        "COVID-19 case numbers over the winter months, the group stands to benefit from an influx "
        "of patients after coronavirus vaccines roll out as elective surgeries return and people "
        "make up for missed treatments.\nKey Takeaways\nAn increasing number of elective "
        "surgeries look set to boost hospital profits in 2021. HCA Healthcare, Inc. ( HCA ) "
        "shares have formed a mini ascending triangle near resistance, indicating that the price "
        "is preparing to push higher. Community Health Systems, Inc. ( CYH ) shares have traded "
        "within a symmetrical triangle over the past four weeks after a sharp rally.\nBelow, "
        "we look at two leading hospital stocks and point out significant technical levels worth "
        "watching.\nHCA Healthcare, Inc. (HCA)\nHCA Healthcare operates general, "
        "acute care hospitals that offer medical and surgical services. Despite suffering a third "
        "quarter year-over-year decline of 3.8% in same facilities admissions and a 6.8% drop in "
        "inpatient surgeries, the healthcare provider reported a 4.9% jump in revenue during the "
        "period to $13.31 billion thanks to tighter cost controls relating to salaries, benefits, "
        "and operating expenses. Looking ahead, the leaner and more efficient hospital chain sits "
        "well positioned to capitalize on higher profit margins as it increases its patient "
        "intake next year. HCA Healthcare stock has a market capitalization of $53.87 billion and "
        "is trading 14.94% higher in the past month, outperforming the industry average by around "
        "5% as of Dec. 9, 2020.\nHCA shares have formed a mini ascending triangle near a "
        "period of two-year resistance at $147, indicating that the price is preparing for its "
        "next push higher. Moreover, the moving average convergence divergence (MACD) indicator "
        "recently crossed back above its trigger line to generate a buy signal. Those who enter "
        "here should consider using a trailing stop to let profits run. For instance, "
        "traders could remain in the position until the price closes below a fast period moving "
        "average, such as the 10-day simple moving average (SMA).\nTradingView.com\nThe "
        "moving average convergence divergence (MACD) is a trend-following momentum indicator "
        "that shows the relationship between two moving averages of a security's price. The MACD "
        "is calculated by subtracting the 26-period exponential moving average (EMA) from the "
        "12-period EMA.\nCommunity Health Systems, Inc. (CYH)\nWith a market cap of $1 "
        "billion, Community Health Systems owns and leases general acute care hospitals located "
        "in non-urban and urban markets. The Tennessee-based hospital operator saw third quarter "
        "admission drop 13% from a year ago, contributing to a 3.7% decline in revenue for the "
        "period. However, the company posted a quarterly net income of 18 cents per share as "
        "lower expenses helped offset reduced patient volumes. Like HCA Healthcare, "
        "the trimmed-back medical facilities giant stands ready to grow profits as it ups "
        "elective surgeries after the pandemic. As of Dec. 9, 2020, Community Health Systems "
        "stock has gained 191% year to date but retraced 12.28% over the past month.\nThe "
        "share price has traded within a symmetrical triangle over the past four weeks after a "
        "sharp rally. Those who anticipate a continuation of the uptrend should think about using "
        "the measured move technique to book profits. To do this, calculate in dollars the leg "
        "higher that preceded the pattern and add that amount to the triangle's upper trendline. "
        "This projects a profit target of $14.99 ($6.22 + $8.77). Protect trading capital with a "
        "stop-loss order placed under the Nov. 3 low at $7.05.\nTradingView.com\nAn "
        "uptrend describes the price movement of a financial asset when the overall direction is "
        "upward. In an uptrend, each successive peak and trough is higher than the ones found "
        "earlier in the trend. The uptrend is therefore composed of higher swing lows and higher "
        "swing highs .\nDisclosure: The author held no positions in the aforementioned "
        "securities at the time of publication."
    )
    assert r["created_at"] == "2020-12-09T00:00:00+00:00"
    assert r["tags"] == ["article", "investopedia.com"]
    assert r["title"] == "2 Hospital Stocks Set to Benefit Beyond the Pandemic"
