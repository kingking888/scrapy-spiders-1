"""Test suit for AgfaxSpider."""

from agblox.spiders.agriculturecom.wheat import AgriculturecomWheatSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return AgriculturecomWheatSpider()


@pytest.fixture()
def last_page_spider():
    s = AgriculturecomWheatSpider()
    s.first_page = False
    return s


headers = headers(AgriculturecomWheatSpider.host_header)
headers["User-Agent"] = AgriculturecomWheatSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            AgriculturecomWheatSpider.url,
            headers,
            [
                "https://www.agriculture.com/crops/wheat/nation-s-best-wheat-yield-tops-200-bushels-per-acre",
                "https://www.agriculture.com/three-farm-daughters-launches-new-product-portfolio-powered-by-goodwheat",
                "https://www.agriculture.com/crops/wheat/arcadia-biosciences-partners-with-three-farm-daughters-to-market-and-develop-goodwheat",
                "https://www.agriculture.com/news/crops/basf-powerpollen-announce-research-collaboration-for-hybrid-wheat",
                "https://www.agriculture.com/news/crops/kansas-wheat-tour-total-agency-estimates-284-million-bushel-crop",
                "https://www.agriculture.com/news/crops/wheat-tour-day-2-42-bushels-per-acre",
                "https://www.agriculture.com/news/crops/wheat-tour-day-1-41-to-51-bushels-per-acre",
                "https://www.agriculture.com/news/crops/winter-wheat-crop-is-in-tough-shape-growers-say",
                "https://www.agriculture.com/crops/wheat/pivot-bio-ramps-up-funding-announces-new-wheat-product",
                "https://www.agriculture.com/crops/wheat?page=1",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    print(r)
    assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.agriculture.com/crops/wheat?page=47",
            headers,
            [
                "https://www.agriculture.com/crops/wheat/production/Some-wheat-breaks-dormancy-due-to-mild-winter-weather_145-ar268",
                "https://www.agriculture.com/crops/wheat/technology/Two-new-broadleaf-control-options-for-wheat-growers_147-ar164",
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
            "https://www.agriculture.com/crops/wheat/arcadia-biosciences-partners-with-three-farm-daughters-to-market-and-develop-goodwheat",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Arcadia Biosciences, Inc. has announced the execution of a term sheet to form a "
        "strategic business venture with Three Farm Daughters, LLLP , a majority female-owned "
        "North Dakota-based consumer food company. The agreement will enable the entities to "
        "develop and market food products using Arcadia’s patented non-GMO GoodWheat technology."
        "\nThe firms will develop Three Farm Daughters-branded food products such as flours, "
        "pastas, and crackers that leverage the enhanced nutritional profiles of GoodWheat "
        "ingredients. Three Farm Daughters products will be sold in grocery stores, on Amazon, "
        "and through the company’s e-commerce site .\n“Three Farm Daughters shares our "
        "commitment to healthy, high-quality food ingredients and clean labels,” said Matthew "
        "Plavan, president and CEO of Arcadia Biosciences, in a news release. “We are excited to "
        "bring our GoodWheat ingredients to market under the Three Farm Daughters brand and look "
        "forward to new and continued innovation to meet growing consumer demand for healthier "
        "food options.” Arcadia’s GoodWheat portfolio of specialty wheat ingredients contain up "
        "to 10 times the dietary fiber of traditional wheat, up to 65% less allergenic gluten, "
        "and nearly 30% fewer calories per serving than traditional wheat.\n“At Three Farm "
        "Daughters, we are passionate about healthful food and uncompromising when it comes to "
        "quality, taste, and performance,” said Mollie Ficocello, president and co-founder of "
        "Three Farm Daughters, in a news release. “Our family has proudly grown GoodWheat wheat "
        "varieties for years, and we know firsthand the difference healthier, quality ingredients "
        "make in our diets and lifestyles. And now, we are thrilled to bring our products to the "
        "market and help consumers take the guesswork out of healthy eating with our Three Farm "
        "Daughters brand.”\nThree Farm Daughters will launch its first product – a refined, "
        "non-enriched wheat flour for everyday baking – in September. Sales of baking staples "
        "such as flour, baking powder, baking soda, and yeast have been at an all-time high "
        "during the COVID-19 pandemic; Nielsen reports consumers spent 126% more on flour in "
        "March and 105% more in April than in 2019.\nArcadia and Three Farm Daughters are "
        "expected to execute definitive agreements in due course."
    )
    assert r["created_at"] == "2020-08-14T00:00:00+00:00"
    assert (
        r["title"]
        == "Arcadia Biosciences partners with Three Farm Daughters to market and develop GoodWheat products"
    )
