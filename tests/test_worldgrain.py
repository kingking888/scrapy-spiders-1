"""Test suit for World-Grain."""

from agblox.spiders.helpers import headers
from agblox.spiders.worldgrain import WorldGrainSpider
import pytest


@pytest.fixture()
def spider():
    return WorldGrainSpider()


headers = headers(WorldGrainSpider.host_header)
headers["User-Agent"] = WorldGrainSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            WorldGrainSpider.url,
            headers,
            [
                "https://www.world-grain.com/articles/14537-china-rejects-claim-its-imports-are-cause-for-high-global-grain-prices",
                "https://www.world-grain.com/articles/14534-syrias-tartous-port-silo-sustains-damage-in-fire",
                "https://www.world-grain.com/articles/14533-grain-foods-foundation-ramps-up-breadbasket-checkoff-outreach",
                "https://www.world-grain.com/articles/14530-wheat-flour-finds-outlet-in-value-added-category",
                "https://www.world-grain.com/articles/14529-cftc-approves-mihs-acquisition-of-mgex",
                "https://www.world-grain.com/articles/14527-europe-catches-up-on-winter-grain-planting-with-favorable-weather",
                "https://www.world-grain.com/articles/14526-denmark-showing-success-in-whole-grain-programs",
                "https://www.world-grain.com/articles/14525-ukraine-has-used-two-thirds-of-wheat-export-quota",
                "https://www.world-grain.com/articles/14524-indias-soybean-production-remains-steady",
                "https://www.world-grain.com/articles/14523-us-cpi-for-baked-foods-cereals-rises-in-october",
                "https://www.world-grain.com/articles/topic/1024?page=2",
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
            "https://www.world-grain.com/articles/topic/1024?page=334",
            headers,
            [
                "https://www.world-grain.com/articles/4159-u-s-rough-rice-stocks-down-15-from-year-ago",
                "https://www.world-grain.com/articles/4162-u-s-wheat-stocks-down-15-corn-up-30",
                "https://www.world-grain.com/articles/4106-corn-miller-celebrates-new-8-million-line",
                "https://www.world-grain.com/articles/4160-u-s-soybean-plantings-reach-record-high",
                "https://www.world-grain.com/articles/3593-cargill-to-close-soybean-processing-operation",
                "https://www.world-grain.com/articles/3588-canada-sets-26-million-tonne-canola-goal",
                "https://www.world-grain.com/articles/3586-canada-boosts-winter-wheat-research",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 7
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.world-grain.com/articles/14120-focus-on-japan",
            headers,
        ),
    ],
)
def test_created_at(spider, response):
    r = next(spider.parse_article(response))
    assert r["created_at"] == "2020-08-19T00:00:00+00:00"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.world-grain.com/articles/14143-coceral-sees-further-drop-in-eu-grain-output",
            headers,
        ),
    ],
)
def test_text_ony(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == """BRUSSELS, BELGIUM — COCERAL sees 2020 grain production in the European Union (including the UK) declining in its most recent forecast released on Aug. 24. In its fourth forecast of the season, COCERAL projects the total 2020 grain crop at 295.2 million tonnes, down from 299.2 million tonnes in its previous forecast and 16.1 million tonnes lower than the 2019 crop of 311.6 million tonnes. Wheat production (excluding durum) is seen at 129.1 million tonnes, down from the previous 129.7 million tonnes and from last year’s 146.8 million tonnes. Significant downward revisions in France and the Balkan countries are not completely offset by upward revisions in Poland, the Baltic countries, and Scandinavia. The EU’s 2020 barley production is now forecast at 62.5 million tonnes, down from the 63.4 million tonnes seen in the previous forecast, but up from 62.1 million last year. The downward revision is mainly due to lower yields in France. The EU’s 2020 corn crop is revised down to 64.6 million tonnes from the previous forecast of 66.8 million tonnes. Last year’s crop was at 64.8 million tonnes. Hot and dry weather has reduced yield potential in France, Germany and the Balkan countries. The 2020 rapeseed production forecast for the EU-27+UK has been revised up from 16.5 million tonnes to 17 million tonnes as actual yields in Germany, Poland and the Baltic countries were better than previously expected. Last year’s crop stood at 16.9 million tonnes. COCERAL represents the interests of the European trade in grains and oilseeds, feedstuffs, rice , olive oil , oils and fats and agro-supply toward the European Union and international institutions, international bodies and stakeholders."""
    )


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.world-grain.com/articles/14198-company-to-handle-sohar-flour-mills-wheat-imports",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == """MUSCAT, OMAN — C. Steinweg Oman LLC, the operator of the general cargo terminal at Sohar Port in Oman, extended its agreement to handle wheat import shipments for Sohar Flour Mills LLC. Sohar Flour Mills is expected to begin its own wheat discharge operations in the first quarter of 2021 at the port. Until then, C. Steinweg Oman will discharge the wheat import shipments and transport the cargo into the warehouse of Sohar Flour Mills. In order to support Oman and its citizens during the coronavirus (COVID-19) pandemic, C. Steinweg Oman has reduced its handling charges to Sohar Flour Mills to boost the import of additional wheat and enhance Oman food security and sustainability. Both parties said they look forward to continuing their collaboration and business relationship."""
    )
    assert r["created_at"] == "2020-09-08T00:00:00+00:00"
    assert r["tags"] == ["wheat", "article", "world-grain.com"]
    assert r["title"] == "Company to handle Sohar Flour Mills wheat imports"
