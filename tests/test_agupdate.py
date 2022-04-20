"""Test suit for AgUpdateCornSpider."""

from agblox.spiders.agupdate import AgupdateSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return AgupdateSpider()


headers = headers(AgupdateSpider.host_header)
headers["User-Agent"] = AgupdateSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            AgupdateSpider.url,
            headers,
            [
                "https://www.agupdate.com/rural_life/direct-federal-aid-to-farmers-predicted-to-more-than-double-in-2020-driving-forecast-of/article_ba145918-64ae-518d-bc38-da3942f97e5b.html",
                "https://www.agupdate.com/iowafarmertoday/markets/crop/grain-market-could-see-correction/article_53c4f446-3418-11eb-98f8-a3616a0adfbf.html",
                "https://www.agupdate.com/iowafarmertoday/news/crop/60-inch-corn-rows-work-in-certain-operations/article_91bf240e-3415-11eb-9536-b7a48cc4de5a.html",
                "https://www.agupdate.com/rural_life/epa-misses-renewable-fuel-standard-deadline-may-punt-biofuel-blending-decision-to-biden-administration/article_44e962df-7ec9-542f-8db9-b7e45561a15b.html",
                "https://www.agupdate.com/midwestmessenger/news/crop/herbicides-for-corn-dry-bean-rotation-in-nebraska/article_f6d0b8a6-2e9a-11eb-9a24-87e57059b3e9.html",
                "https://www.agupdate.com/iowafarmertoday/news/crop/first-corn-shows-consistent-yields-outside-extreme-weather-zones/article_647910b8-2e89-11eb-972f-ab3bb290fd34.html",
                "https://www.agupdate.com/crops/using-data-for-better-seed-selection/article_68a868d6-2e7b-11eb-97a9-0f7c6dc117b7.html",
                "https://www.agupdate.com/farmandranchguide/markets/crop/soybean-market-sees-nice-rally-ahead-of-thanksgiving/article_2509b81c-2e05-11eb-9481-832249348abf.html",
                "https://www.agupdate.com/iowafarmertoday/news/state-and-regional/firefighters-farmers-curb-huge-field-fire/article_1aeeaec8-2e64-11eb-9dc8-c3bf708a2ee5.html",
                "https://www.agupdate.com/farmandranchguide/markets/crop/corn-market-reaches-rare-december-high/article_02790524-2e04-11eb-82c3-ffc0bf775c51.html",
                "https://www.agupdate.com/search/?k=%22corn%22&l=10&app%5B0%5D=editorial&o=10",
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
            "https://www.agupdate.com/search/?k=%22corn%22&l=10&app%5B0%5D=editorial&o=7460",
            headers,
            [
                "https://www.agupdate.com/theprairiestar/agweekly/news/livestock/beef-industry-names-vision-awards-winners/article_738b113b-a452-5086-8702-c9b3affdebc1.html",
                "https://www.agupdate.com/theprairiestar/agweekly/news/livestock/sec-schafer-addresses-cattle-issues-at-industry-convention/article_afe99ffa-45ef-5567-8a34-800fcd3bb114.html",
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
            "https://www.agupdate.com/iowafarmertoday/markets/crop/smaller-production-helps-sustain-grain-rally/article_f0a5bb2c-0d8c-11eb-ac78-a7920d4ea510.html",
            headers,
        ),
    ],
)
def test_text_ony(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == """Grain futures contracts have been on the rise in the past month as supply tightens and demand rises, according to the latest monthly USDA report. In the Oct. 9 WASDE report, corn and soybeans both saw estimated production reduced, as corn is expected to have a 178.4 bushel per acre yield and soybeans a 51.9 bushel per acre yield. Estimated acres also dropped overall in both crops after drought and storm damage affected many Midwest areas. After the report was released the markets did rally, highlighted by a 25 cent higher settlement in the March 2021 soybean market, and Ami L. Heesch of CHS Hedging said the jumps have led many farmers to dip their toes back in the market. “The soybeans continue their trek to higher levels on smaller stocks and ongoing demand for U.S. beans,” she said. “Farmers have sold into the rally while country elevators wait for trains to load beans out for the new crop program.” Soybean future contracts had been on the rise in anticipation of this report, and Mike Zuzolo of Global Commodity Analytics said this simply “fed the bulls.” But finding out if these upper-$10 prices are here to stay or simply a blip on the radar might take a little more time. “While I’m not ready to suggest the soybeans are the leader to the downside, I do think that we’re at price levels and spread levels where corn and wheat need to support soy if it’s going to break through the $10.90 area again,” Zuzolo said. World dynamics are also playing into hopes for continued demand for U.S. crops, as South American weather continues to play a factor for planting. This has particularly helped the soybean futures market as continued dry weather in the southern hemisphere will limit world supplies. “I’d expect this to become more supportive as we head through the week if we indeed see lighter rainfall totals by Friday afternoon (in Brazil),” Zuzolo said. {{description}} Email notifications are only sent once a day, and only if there are new matching items."""
    )


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.agupdate.com/northwest-missouri-soil-in-good-shape-after-flood/article_a53d74b0-1479-11eb-8547-0f00dbe78d96.html",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == """Larry Hecker harvests soybeans in Atchison County. Much of Hecker’s acres were under water last year. FAIRFAX, Mo. — A soggy spring and a dry summer seem pretty minor to Larry Hecker. A year ago, much of his Northwest Missouri ground was under water after the Missouri River came pouring through a nearby levee. “We didn’t even get to work this field since it was under water so long,” says Hecker, who farms in Atchison County. Despite the flooding, he says the ground worked up well when he started spring planting. “This gumbo, it was in pretty good shape,” Hecker says. “I don’t think it has ever worked up any better.” Bean yields were in the 50-60 bushels per acre range, he said Oct. 14. He expected to start harvesting corn in a few days. “We had some strong winds come through here the other night, and it took everything but the stalks and ears,” he says. Hecker says he has heard of corn yields in the 200-bushel range. He says the wet spring was hard on some of the crop, particularly river bottom ground. “I’m hearing of good yields in the hilly ground,” Hecker says. Jeff DeYoung is livestock editor for Iowa Farmer Today, Missouri Farmer Today and Illinois Farmer Today. {{description}} Email notifications are only sent once a day, and only if there are new matching items."""
    )
    assert r["created_at"] == "2020-10-23T14:00:00-05:00"
    assert r["tags"] == ["article", "agupdate.com"]
    assert r["title"] == "Northwest Missouri soil in good shape after flood"
