"""Test suit for SoybeansandcornSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.soybeansandcorn import SoybeansandcornSpider
import pytest


@pytest.fixture()
def spider():
    return SoybeansandcornSpider()


headers = headers(SoybeansandcornSpider.name)
headers["User-Agent"] = SoybeansandcornSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            SoybeansandcornSpider.url,
            headers,
            [
                "http://soybeansandcorn.com/news/Nov9_20-Brazil-Importing-US-Soybeans",
                "http://soybeansandcorn.com/news/Nov6_20-Soybeans-are-Not-a-Major-Contributor-to-Fires-in-Brazilian-Amazon",
                "http://soybeansandcorn.com/news/Nov4_20-Worrisome-Long-Range-Forecast-for-Southern-Brazil",
                "http://soybeansandcorn.com/news/Nov4_20-202021-Argentina-Corn-30-Planted-Soybeans-2-3-Planted",
                "http://soybeansandcorn.com/news/Nov2_20-Soybean-and-Corn-Prices-Continue-to-Set-Records-in-Brazil",
                "http://soybeansandcorn.com/news/Oct30-20-Farmers-in-N-Mato-Grosso-Working-Double-Shifts-Planting-Soy",
                "http://soybeansandcorn.com/news/Oct29_20-Farmers-in-Parana-Almost-Double-Soybean-Planting-in-One-Week",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    # the website is one giant page, would be impractical to put all of them in test
    assert r[: len(expected)] == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "http://soybeansandcorn.com/news/Nov9_20-Brazil-Importing-US-Soybeans",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Back\nNovember 9, 2020\nBrazil Importing U.S. Soybeans\nAuthor: "
        "Michael Cordonnier/Soybean & Corn Advisor, Inc.\nBrazil is the world's "
        "largest producer and exporter of soybeans and yet it was announced last "
        "week that Brazil is importing soybeans from the United States to meet "
        "domestic demands. A maritime agency announced last week that a vessel was "
        "being loaded in Louisiana with 38,000 tons of soybeans destined to arrive "
        "at the Port of Paranagua in southern Brazil on November 20th. There are "
        "additional reports of more sales of U.S. soybeans to Brazil.\nThese "
        "sales already represent the largest since 1997 when Brazil imported more "
        "than 600,000 tons of U.S. soybeans. These imports have occurred after the "
        "Brazilian government temporarily suspended the 8% tariff for grain "
        "imported from non-Mercosul countries. The suspension will remain in place "
        "for soybeans until January 15th and for corn until March 31st.\nThere "
        "were concerns that it would be difficult to import soybeans into Brazil "
        "because bulk shipments of soybeans from then U.S. might contain GMO "
        "soybean varieties that have not been approved in Brazil. That issue was "
        "resolved when the Brazilian Minister of Agriculture issued a decree that "
        "Brazil would accept GMO varieties approved in the U.S.\nDomestic "
        "soybean prices in Brazil are at record high levels due to the very tight "
        "domestic supplies. Brazil exported record amounts of soybeans earlier this "
        "year due to a 35% devaluation of the Brazilian currency which made "
        "Brazilian soybeans very competitive in the world market. Additionally, "
        "China focused their attention on Brazilian soybeans in the midst of a "
        "trade dispute with the U.S. Of the soybeans imported by China between "
        "April and September of this year, 86% was from Brazil.\nThe start of "
        "the 2020/21 soybean planting in Brazil was delayed due to dry weather, "
        "so that means the soybean harvest will be delayed as well. As a result, "
        "there may be additional imports of U.S. soybeans into Brazil enabling "
        "crushers to keep operating until the Brazilian soybean harvest starts next "
        "February."
    )
    assert r["created_at"] == "2020-11-09T00:00:00+00:00"
    assert r["tags"] == ["article", "soybeansandcorn.com"]
    assert r["title"] == "Brazil Importing U.S. Soybeans"
