"""Test suit for AgfaxSpider."""

from agblox.spiders.agriculturecom.crop_markets import AgriculturecomCropmarketSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return AgriculturecomCropmarketSpider()


@pytest.fixture()
def last_page_spider():
    s = AgriculturecomCropmarketSpider()
    s.first_page = False
    return s


headers = headers(AgriculturecomCropmarketSpider.host_header)
headers["User-Agent"] = AgriculturecomCropmarketSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            AgriculturecomCropmarketSpider.url,
            headers,
            [
                "https://www.agriculture.com/markets/analysis/crops/is-the-bear-on-the-run",
                "https://www.agriculture.com/markets/analysis/crops/new-numbers-and-a-new-outlook-for-the-corn-and-soybean-markets",
                "https://www.agriculture.com/markets/analysis/crops/bullish-argument-for-corn",
                "https://www.agriculture.com/markets/analysis/crops/make-sales-and-re-own-on-paper",
                "https://www.agriculture.com/markets/analysis/crops/wheat-spreads-widen-further",
                "https://www.agriculture.com/news/business/despite-coronavirus-pandemic-farmers-plan-to-plant-a-record-corn-crop",
                "https://www.agriculture.com/markets/analysis/crops/al-kluis-changing-with-the-times",
                "https://www.agriculture.com/markets/analysis/crops/al-kluis-trade-war-takes-a-toll-on-revenue",
                "https://www.agriculture.com/markets/analysis/crops/protection-in-the-soybean-market",
                "https://www.agriculture.com/markets/analysis/crops?page=1",
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
            "https://www.agriculture.com/markets/analysis/crops?page=577",
            headers,
            [
                "https://www.agriculture.com/markets/analysis/soybeans/Time-to-sell-soybeans_10-ar35",
                "https://www.agriculture.com/markets/analysis/wheat/Iraq-confirms-US-wheat-purchase_11-ar23",
                "https://www.agriculture.com/markets/analysis/corn/Kevin-McNew-Corn-basis-rally-stalls_9-ar18",
                "https://www.agriculture.com/markets/analysis/soybeans/Opportunity-for-soybean-sales-analysts-say_10-ar7",
                "https://www.agriculture.com/markets/analysis/corn/Domestic-useage-key-to-corn-futures-prices_9-ar1",
            ],
        ),
    ],
)
def test_last_page(last_page_spider, response, expected):
    r = [e.url for e in last_page_spider.parse(response)]
    assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.agriculture.com/markets/analysis/crops/new-numbers-and-a-new-outlook-for-the-corn-and-soybean-markets",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "The November USDA Supply and Demand report had major surprises for the corn and soybean "
        "markets, and consequently, long-term availability of these commodities is a potential "
        "concern. The highlights of the report were reductions in yield and lower carryout. Yield "
        "for both was below expectations, which means this was a major surprise. Just as "
        "important, a significant increase in expected exports for corn dropped projected "
        "carryout well beyond expectations.\nThe highlights of the report were corn yield "
        "coming in at 175.8 bushels an acre as compared to a forecast of 177.5 and last month’s "
        "figure of 178.4. This 2.6 bushel per acre reduction was a supportive factor, as was a "
        "significant increase to projected exports. The new expected sales figure is 2.650 "
        "billion bushels. This compares to 2.325 last month and 1.778 a year ago. Prior to the "
        "report projected carry out was 2.167 billion bushels, a somewhat comfortable number. The "
        "new figure is now 1.702 billion, a decline of 465 million bushels from the previous "
        "month and 350 million bushels lower than the pre-report average estimate of analysts. "
        "Perhaps the most eyepopping number, however, is the average farm price for the 2020/21 "
        "growing season now forecasted to be $4.00 versus $3.60 on the October "
        "report.\nSoybeans had a somewhat similar story with yield projections down 1.2 "
        "bushels an acre at 50.7. The average pre-report estimate was 51.7 million. Carry out is "
        "now forecasted at 190 million bushels. This was 100 million bushels less than last month "
        "and compares to 523 million bushels for the same time a year ago. Two years ago, "
        "projected carryout was 909 million bushels. Exports as well as other usage numbers "
        "remained unchanged in this month’s report.\nThese raw numbers make for a very "
        "different potential price and supply outlook. Crop production elsewhere in the world "
        "must be near perfect, otherwise it is likely that importing countries will continue to "
        "come to the US. Consider that yield at 175.8 is still 7 bushels an acre better than last "
        "year, and soybean yield at 50.7 is still 3.3 bushels an acre larger than a year ago. "
        "Overall, we would call these good, or even very good crops. We hesitate to use the word "
        "great, as yield potential declined late in the growing season due to dry weather. "
        "Soybean production from South America must be large and near ideal. There is the real "
        "potential that weather developments in either Brazil or Argentina could create a "
        "rationing effect for soybeans. This implies prices could move higher in order to keep "
        "inventory on hand. While not forecasting this to occur it is a real and distinct "
        "possibility. On the other hand, while becoming tight, 1.7 billion bushels of corn carry "
        "out is probably not enough to suggest rationing unless there is a wholesale reduction in "
        "southern Hemisphere production. Still, tighter carry out numbers make for a more "
        "sensitive market and price volatility.\nMarketing decisions are probably not getting "
        "easier. In fact, bull markets often make selling or buying decisions more challenging "
        "and stressful. To help alleviate stressful marketing decisions, the best approach is "
        "likely to be one of balance between cash sales, re-ownership and using put options to "
        "establish price floors while leaving inventory on priced. Connect with your advisor to "
        "have in-depth and thorough conversation on how they can help you achieve this goal of "
        "being balanced. Marketing is ongoing and needs adjusting continuously, especially in "
        "volatile markets.\nIf you have comments, questions, or suggestions, contact Bryan "
        "Doherty at Total Farm Marketing. You can reach him at 1-800-top-farm, extension "
        "444.\nFutures trading is not for everyone. The risk of loss in trading is "
        "substantial. Therefore, carefully consider whether such trading is suitable for you in "
        "light of your financial condition. Past performance is not necessarily indicative of "
        "future results."
    )
    assert r["created_at"] == "2020-11-16T00:00:00+00:00"
    assert r["title"] == "New numbers and a new outlook for the corn and soybean markets"
