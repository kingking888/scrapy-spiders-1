"""Test suit for AgfaxSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.thecropsite import ThecropsiteSpider
import pytest


@pytest.fixture()
def spider():
    return ThecropsiteSpider()


headers_dict = headers(ThecropsiteSpider.host_header)
headers_dict["User-Agent"] = ThecropsiteSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            ThecropsiteSpider.url,
            headers_dict,
            [
                "https://www.thecropsite.com/news/17968/the-benefits-of-bringing-cattle-and-crops-together",
                "https://www.thecropsite.com/news/17936/global-food-commodity-prices-rebounded-in-june",
                "https://www.thecropsite.com/news/17938/fao-global-food-markets-brace-for-uncertainty-in-20-21-due-to-covid19",
                "https://www.thecropsite.com/news/17945/going-with-the-grain-to-combat-diabetes",
                "https://www.thecropsite.com/news/17960/newly-discovered-plant-gene-could-boost-phosphorus-intake",
                "https://www.thecropsite.com/news/17921/ahdb-large-stocks-weigh-on-uk-wheat-supply-demand",
                "https://www.thecropsite.com/news/17917/brazilian-agricultural-exports-grow-175-in-2020",
                "https://www.thecropsite.com/news/17911/farm-market-id-offers-onfarm-grain-storage-data-to-agribusinesses",
                "https://www.thecropsite.com/news/17910/current-house-farm-bill-fails-to-meet-needs-of-family-farmers-says-nfu-us",
                "https://www.thecropsite.com/news/17795/usda-reports-winter-wheat-surprises-with-second-lowest-planting-since-1913",
                "https://www.thecropsite.com/news/17758/rabobank-outlook-2016-bearish-grains-bullish-for-hogs",
                "https://www.thecropsite.com/news/17735/weather-el-nios-global-impact-us-november-outlook",
                "https://www.thecropsite.com/news/17728/european-gm-optout-would-put-rural-jobs-at-risk",
                "https://www.thecropsite.com/news/17723/the-scoop-on-poop-why-is-manure-important",
                "https://www.thecropsite.com/news/17711/allendale-inc-what-will-wasde-mean-for-grain-prices",
                "https://www.thecropsite.com/news/17676/most-eu-food-waste-avoidable",
                "https://www.thecropsite.com/news/17679/community-spirit-drives-americans-to-support-local-food",
                "https://www.thecropsite.com/news/17678/farmers-seeking-next-step-in-precision-ag-choose-uavs",
                "https://www.thecropsite.com/news/17672/us-agricultural-input-costs-up-in-2014",
                "https://www.thecropsite.com/news/17677/agritechnica-is-coming-to-germany-in-november-2015",
                "https://www.thecropsite.com/news/17626/substantial-increase-in-old-crop-wheat-carryover",
                "https://www.thecropsite.com/news/17621/ukrainian-wheat-crop-potential-boosted",
                "https://www.thecropsite.com/news/17622/cme-better-drought-conditions-cause-pasture-wheat-improvement",
                "https://www.thecropsite.com/news/17619/planting-progresses-regardless-of-rain",
                "https://www.thecropsite.com/news/17613/the-bullish-risk-of-being-too-bearish",
                "https://www.thecropsite.com/news/17608/bayer-cropscience-opens-breeding-trait-development-station",
                "https://www.thecropsite.com/news/17599/earlier-flowering-can-help-wheat-cope-with-hotter-world",
                "https://www.thecropsite.com/news/17602/cme-good-crop-plantings-cause-futures-decline",
                "https://www.thecropsite.com/news/17584/what-will-lift-the-weight-from-the-market",
                "https://www.thecropsite.com/news/17548/uk-milling-premium-still-near-this-seasons-low",
                "https://www.thecropsite.com/news/category/61/wheat/vars/offset/30",
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
            "https://www.thecropsite.com/news/category/61/wheat/vars/offset/3810/",
            headers_dict,
            [
                "https://www.thecropsite.com/news/5476/wheat-crop-threatened-by-drought",
                "https://www.thecropsite.com/news/5475/indian-state-introduces-rice-and-wheat-subsidy-for-poor",
                "https://www.thecropsite.com/news/5467/russia-sells-cuba-humanitarian-milling-wheat",
                "https://www.thecropsite.com/news/5452/looking-beyond-us-borders",
                "https://www.thecropsite.com/news/5453/world-grain-stock-will-reach-8year-high",
                "https://www.thecropsite.com/news/5447/scientists-pursue-mineralrich-wheat-variant",
                "https://www.thecropsite.com/news/5436/the-2010-cereal-recommended-list",
                "https://www.thecropsite.com/news/5434/research-before-selecting-corn-varieties",
                "https://www.thecropsite.com/news/5427/any-chance-for-a-recovery-in-crop-prices",
                "https://www.thecropsite.com/news/5421/weak-durum-demand-could-prompt-crop-switch",
                "https://www.thecropsite.com/news/5423/french-wheat-pricing-and-quality-must-be-more-competitive",
                "https://www.thecropsite.com/news/5408/india-to-sell-up-to-3m-tonnes-of-rice-and-wheat",
                "https://www.thecropsite.com/news/5385/weekly-roberts-report",
                "https://www.thecropsite.com/news/5379/crop-insurance-and-risk-management-decisions-affect-profits",
                "https://www.thecropsite.com/news/5373/cuphea-does-wonders-for-wheat-corn-in-rotations",
                "https://www.thecropsite.com/news/5336/global-crop-prices-roundup",
                "https://www.thecropsite.com/news/5354/egypt-commits-to-nile-basin-crop-investment",
                "https://www.thecropsite.com/news/5360/sure-crop-loss-supplements-for-us-farmers",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            ThecropsiteSpider.url,
            headers_dict,
            [
                "https://www.thecropsite.com/news/17968/the-benefits-of-bringing-cattle-and-crops-together",
                "https://www.thecropsite.com/news/17936/global-food-commodity-prices-rebounded-in-june",
                "https://www.thecropsite.com/news/17938/fao-global-food-markets-brace-for-uncertainty-in-20-21-due-to-covid19",
            ],
        ),
    ],
)
def test_limit_reached(spider, response, expected):
    spider.last_url = (
        "https://www.thecropsite.com/news/17945/going-with-the-grain-to-combat-diabetes/"
    )
    r = [e.url for e in spider.parse(response)]
    assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.thecropsite.com/news/17337/australian-farmers-supportive-of-foreign-investment/",
            headers_dict,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["url"]
        == "https://www.thecropsite.com/news/17337/australian-farmers-supportive-of-foreign-investment/"
    )
    assert (
        r["text"]
        == r"""News Australian Farmers Supportive of Foreign Investment 13 February 2015 AUSTRALIA- Farmers from Western Australia are overwhelmingly supportive of Chinese and other foreign investment, new research has revealed. Despite researchers expecting farmers from WA's wheatbelt to say foreign investment had destroyed local employment opportunities and caused a detrimental rise to land prices, they said much the opposite. The research sought a grassroots perspective with bankers, property managers, government department staff members and farmers taking part. "The most interesting results were from the farmers," said Dr Marit Kragt, an assistant professor at the School of Agriculture and Resource Economics at the University of Western Australia "We expected them to be quite critical of foreign investment, we expected people to say 'oh they're buying up our land and there 's all these foreigners coming to work on the farms,' but that wasn't the case at all." "We actually didn't find any prejudice against investment from specific countries." "There is a lot of investment from Arabic countries and (south- east Asian countries) that you don't hear much about." "Most of the media attention is on investors from China but there wasn't that many in the wheatbelt where we looked." Researchers expecting farmers to complain that foreign investment had taken jobs away from local people instead were told that the corporate businesses had hired local farmers, local farm managers, bought the inputs from the local area where possible and generated jobs for families. Farmers also said natural resources were managed well. Dr Kragt said foreign investment was particularly helpful to those looking to enter the industry. "If you're just starting out it might be positive to have foreign investment if you're able to lease a foreign-owned farm or foreign-owned land, because you won't have to actually buy the land yourself," she said. The research will be presented to the Australian Agricultural and Resource Economic Society. TheCropSite News Desk Wheat General/Other Markets/Economics"""
    )
    assert r["created_at"] == "2015-02-13T00:00:00+00:00"
    assert r["title"] == "Australian Farmers Supportive of Foreign Investment"
