"""Test suit for AgfaxSpider."""

from agblox.spiders.agriculturecom.corn import AgriculturecomCornSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return AgriculturecomCornSpider()


@pytest.fixture()
def last_page_spider():
    s = AgriculturecomCornSpider()
    s.first_page = False
    return s


headers = headers(AgriculturecomCornSpider.host_header)
headers["User-Agent"] = AgriculturecomCornSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            AgriculturecomCornSpider.url,
            headers,
            [
                "https://www.agriculture.com/crops/corn/new-tech-coming-in-seed-traits",
                "https://www.agriculture.com/crops/corn/13-thoughts-for-seed-selection",
                "https://www.agriculture.com/podcast/successful-farming-radio-podcast/figuring-corn-seeds-per-acre",
                "https://www.agriculture.com/crops/soybeans/all-about-adjuvants",
                "https://www.agriculture.com/crops/corn/how-to-beat-corn-rootworm-in-2021",
                "https://www.agriculture.com/podcast/successful-farming-podcast/dry-corn-with-ground-heat",
                "https://www.agriculture.com/crops/corn/illinois-scientists-rev-up-plant-breeding-for-organic-corn",
                "https://www.agriculture.com/video/iowa-damaged-corn-will-not-be-harvested",
                "https://www.agriculture.com/crops/corn/manage-marestail-and-henbit-this-fall",
                "https://www.agriculture.com/crops/corn?page=1",
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
            "https://www.agriculture.com/crops/corn?page=127",
            headers,
            [
                "https://www.agriculture.com/crops/corn/production/Kill-weeds-while-theyre-small-to-prevent-yield-loss_137-ar646",
                "https://www.agriculture.com/crops/corn/marketing/How-bad-were-2005-corn-yields_138-ar441",
                "https://www.agriculture.com/crops/corn/technology/Study-Adopting-new-Bt-corn-is-ageold-decision-for-farmers_139-ar293",
                "https://www.agriculture.com/crops/corn/production/Corn-after-corn-a-continuous-challenge-for-growers_137-ar275",
                "https://www.agriculture.com/crops/corn/technology/Highlysine-corn-is-first-biotech-trait-from-Renessen_139-ar217",
                "https://www.agriculture.com/crops/corn/technology/Vector-stack-hybrids-clear-regulatory-hurdle_139-ar2",
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
            "https://www.agriculture.com/podcast/successful-farming-radio-podcast/figuring-corn-seeds-per-acre",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == "The number of seeds planted per-acre in a corn field has been increasing annually "
        "over the past two decades. Much of this is because plant breeders continue to improve "
        "the overall stress tolerance of hybrids, and high plant populations do represent a "
        "type of stress.\nBob Nielsen is an agronomy professor at Purdue University . He "
        'says their research is showing that corn eventually reaches a plateau.\n"At the '
        "lower side, as you increase populations you get a pretty strong yield response. But "
        "as the population gets closer and closer to the optimum, the yield response begins to "
        'taper off, and ultimately it just basically plateaus," he says. "And once you reach '
        "the optimum agronomic population, adding more plants simply does not increase yield, "
        'and at some point, will actually decrease yield."\nBecause those last '
        "thousand-seeds-per-acre-or-so result in so few bushels, the economic optimum ends up "
        'being less than the agronomic optimum.\n"Our agronomic optimum, for example '
        'throughout much of Indiana, is a final stand of somewhere around 32,000," he says. '
        '"But because of that response curve and with grain prices being what they are and '
        "feed costs being what they are, our economic optimum tends to be below 30,"
        '000 for many of our soils here in Indiana."\nKnowing the history of successful '
        "stand establishments allows you to convert plant populations to seeding rates. "
        "Nielsen says with today’s planter technologies and seed quality, aiming for a percent "
        "stand of no less than 95% is a realistic goal."
    )
    assert r["created_at"] == "2020-11-16T00:00:00+00:00"
    assert r["title"] == "Figuring Corn Seeds Per Acre"
