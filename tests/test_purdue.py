"""Test suit for PurdueSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.purdue import PurdueSpider
import pytest


@pytest.fixture()
def spider():
    return PurdueSpider()


headers = headers(PurdueSpider.name)
headers["User-Agent"] = PurdueSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            PurdueSpider.url,
            headers,
            [
                "https://ag.purdue.edu/commercialag/ageconomybarometer/ag-barometer-rises-as-crop-prices-rally-and-usda-announces-cfap-2/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/farmer-sentiment-rebounds-as-commodity-prices-rally-and-agriculture-trade-prospects-improve/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/ag-economy-barometer-stable-but-farmers-less-optimistic-about-future/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/farmer-sentiment-rebounds-amidst-ongoing-covid-19-concerns/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/covid-19-continues-to-impact-farmer-sentiment-majority-indicate-economic-assistance-bill-necessary/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/report-ag-barometer-index-drops-below-100-as-coronavirus-disrupts-agriculture/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/farmer-sentiment-plummets-as-coronavirus-concerns-rise/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/optimism-about-current-conditions-pushes-farmer-sentiment-index-to-all-time-high/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/expectations-for-improved-trade-with-china-sends-farmer-sentiment-soaring-2/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/farmers-optimistic-about-the-future-even-as-their-perception-of-current-economic-conditions-drops-2/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/category/report/page/2/",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 11
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://ag.purdue.edu/commercialag/ageconomybarometer/category/report/page/6/",
            headers,
            [
                "https://ag.purdue.edu/commercialag/ageconomybarometer/low-commodity-prices-weigh-producer-sentiment/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/long-term-outlook-strengthens/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/ag-economy-barometer-moves-higher-weather-producers-minds/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/producer-sentiment-settles-lowers-outlook-toward-farmland-remains-favorable/",
                "https://ag.purdue.edu/commercialag/ageconomybarometer/april-2016-report/",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 5
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://ag.purdue.edu/commercialag/ageconomybarometer/ag-barometer-rises-as-crop-prices-rally-and-usda-announces-cfap-2/",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == """U.S. agricultural producers became more optimistic again in September as the Purdue University-CME Group Ag Economy Barometer climbed to 156, the highest reading for the index since the pandemic began last winter and 12 points higher than one-month earlier. The index is up 38 points since July and is 60 points higher than its 2020 low established back in April. In September, producers were more optimistic about both current conditions and the future for agriculture than they were in August. The Current Conditions Index, with a reading of 142, was 18 points higher compared to a month earlier and the Future Expectations Index rose 9 points to a reading of 163. The Ag Economy Barometer is calculated each month from 400 U.S. agricultural producers’ responses to a telephone survey. This month’s survey was conducted from September 21-25, 2020. The improvement in the barometer and its two primary sub-indices occurred against the backdrop of USDA’s September 18 th announcement of the second round of Coronavirus Food Assistance Program (CFAP 2) payments for U.S. agricultural producers. The program provides up to $14 billion in additional assistance to agricultural producers determined to have suffered from market disruptions and costs because of COVID-19. Program details were released on September 21 st , just as data collection for this month’s survey began. Additionally, fall harvested crop prices strengthened from the time data was collected for the August to the September surveys, in a continuation of a rally that got underway in late summer. For example, in west-central Indiana cash corn prices rose nearly $0.20 per bushel from late August to late September, while cash soybean prices rose nearly $1 per bushel. The resulting revenue boost from these two sources likely provided much of the impetus for this month’s 18-point rise in the Index of Current Conditions and the 12-point rise in the Ag Economy Barometer . The improvement in current conditions helped make producers more confident that now is a good time to make large investments in their farming operations than they were in August. The Farm Capital Investment Index rose again in September to a reading of 73, the highest reading of 2020. Helping to confirm the optimism evident in the investment index, fewer producers in September than in August and prior months, said they planned to reduce their machinery purchases compared to a year earlier. Farmers’ optimism carried through to their perspective on farmland values over the upcoming year. More producers in September said they expect farmland values to rise over the next 12 months than in August. The longer-run optimism about farmland values expressed in August continued in September as the percentage of producers expecting farmland values to rise over the next 5 years was unchanged at 59%, which is still the highest reading of this year. Although export sales to China have been rising in recent weeks, producers were, somewhat surprisingly, a bit less optimistic about future agricultural trade prospects in September than they were in August. In September, 58 percent of respondents said they expect ag exports to increase over the next 5 years, down from 67 percent who felt that way in August. The shift occurred because more producers said they expected exports to remain about the same in the future, rather than increase. In a related question, producers were asked whether they expect China to fulfill the food and agricultural import requirements established in the Phase One trade agreement signed earlier this year. Farmers’ opinions were split regarding Phase One’s prospects with just less than half (47%) of respondents indicating they expect China to fulfill its commitment to import food and ag products from the U.S. Increasingly educational events and programs are transitioning to online delivery as a result of the pandemic. Twenty-two percent of respondents to the September survey said they attended an online educational program or field day this year. When asked what aspects of these programs they liked, the two most popular responses were flexible timing of attending and viewing the programs (27%) and the ability to choose topics of interest (21%) followed by quality of presentations (16%), opportunity to earn continuing education credits (14%), and opportunities to ask questions (13%). When asked what aspects of these programs they disliked respondents overwhelmingly pointed to the lack of interaction with other attendees (40%) followed by a poor broadband connection (18%), difficulty in asking questions (17%), and poor quality of presentations (14%). Cover crop usage has received a lot of attention in recent years. To learn more about cover crop usage, this month’s survey included several questions on cover crops. Nearly 4 out of 10 corn/soybean producers in the September survey said they intend to plant at least some cover crops in fall 2020. Two-thirds of the farmers who intend to plant a cover crop this fall have been planting cover crops for more than four years whereas just 7 percent of respondents said this would be the first time they planted a cover crop on their farm. Although nearly 40 percent of corn/soybean producers said they intend to plant cover crops this fall, most of them will only plant cover crops on a portion of their crop acreage. Just over half (52%) of the respondents using cover crops in 2020 said that they intend to plant cover crops on one-third or less of their corn/soybean acreage while 21 percent of the farms in the September survey said they intend to plant cover crops on one-third to as much as two-thirds of their corn/soybean acreage. The remaining 27 percent of producers planting cover crops this fall intend to do so on more than two-thirds of their corn/soybean acreage. Farmers who intend to plant cover crops this fall overwhelmingly (79%) said their primary reason for doing so was to improve soil health and crop yields, while just 1 percent of respondents said it was because of the availability of cost-share funds. Farmer sentiment improved again in September as the Ag Economy Barometer rose 12 points from a month earlier. The rise in the barometer was fueled in large part by producers’ improved perception of current conditions as the Index of Current Conditions rose 18 points above the August reading. USDA’s announcement of the second round of CFAP payments to agricultural producers and the ongoing rally in fall crop prices were likely the two primary drivers behind the improvement in farmer sentiment. Ag producers were also more optimistic about making investments in their farming operation and about the short-run outlook for farmland values than they were in August. Farmers’ opinions regarding whether or not China would fulfill its Phase One trade agreement commitments to the U.S. were split, with slightly less than half expecting China to meet its import commitments. Finally, nearly 40 percent of corn/soybean farmers said they intend to plant cover crops this fall, although a majority of them (52%) said they will plant cover crops on one-third or less of their corn/soybean acreage."""
    )
    assert r["created_at"] == "2020-10-06T00:00:00+00:00"
    assert r["tags"] == ["article", "ag.purdue.edu"]
    assert r["title"] == "Ag Barometer Rises as Crop Prices Rally and USDA Announces CFAP 2"
