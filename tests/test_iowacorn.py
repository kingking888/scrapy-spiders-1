"""Test suit for PurdueSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.iowacorn import IowacornSpider
import pytest


@pytest.fixture()
def spider():
    return IowacornSpider()


headers = headers(IowacornSpider.host_header)
headers["User-Agent"] = IowacornSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            IowacornSpider.url,
            headers,
            [
                "https://www.iowacorn.org/about/news/icpb-hosts-virtual-meetings-with-mexican-and-southeast-asian-trade-teams/",
                "https://www.iowacorn.org/about/news/cropstv-transitions-live-meetings-to-online-delivery/",
                "https://www.iowacorn.org/about/news/iowa-corn-contributes-to-beef-up-iowa-program/",
                "https://www.iowacorn.org/about/news/iowa-corn-growers-association-welcomes-next-generation-fuels-act/",
                "https://www.iowacorn.org/about/news/iowa-corn-growers-association-pac-announces-candidate-endorsements/",
                "https://www.iowacorn.org/about/news/icga-usda-announces-additional-funding-under-cfap/",
                "https://www.iowacorn.org/about/news/icga-scores-a-win-as-epa-denies-dozens-of-gap-year-ethanol-waivers/",
                "https://www.iowacorn.org/about/news/icga-relays-corn-farmer-derecho-and-drought-concerns-to-sec-sonny-perdue/",
                "https://www.iowacorn.org/about/news/icgas-letter-to-us-secretary-of-agriculture-sonny-perdue/",
                "https://www.iowacorn.org/about/news/icga-delegates-adopt-policies-impacting-iowa-corn-farmers-at-annual-grassroots-summit/",
                "https://www.iowacorn.org/about/news/?page=2",
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
            "https://www.iowacorn.org/about/news/?page=33",
            headers,
            [
                "https://www.iowacorn.org/about/news/tools-for-the-future-crop-fair-feb-16-in-missouri-valley-provides-essential-management-tips/",
                "https://www.iowacorn.org/about/news/tools-for-the-future-crop-fair-feb-17-in-creston-provides-essential-management-tips/",
                "https://www.iowacorn.org/about/news/tools-for-the-future-crop-fair-feb-13-in-red-oak-provides-essential-management-tips/",
                "https://www.iowacorn.org/about/news/tools-for-the-future-crop-fair-feb-12-in-mason-city-provides-essential-management-tips/",
                "https://www.iowacorn.org/about/news/tools-for-the-future-crop-fair-feb-5-in-elkader-provides-essential-management-tips/",
                "https://www.iowacorn.org/about/news/tools-for-the-future-crop-fair-feb-5-in-ames-provides-essential-management-tips/",
                "https://www.iowacorn.org/about/news/tools-for-the-future-crop-fair-feb-5-in-algona-provides-essential-management-tips/",
                "https://www.iowacorn.org/about/news/tools-for-the-future-crop-fair-feb-4-in-paullina-provides-essential-management-tips/",
                "https://www.iowacorn.org/about/news/tools-for-the-future-crop-fair-jan-29-in-fayette-provides-essential-management-tips/",
                "https://www.iowacorn.org/about/news/tools-for-the-future-crop-fair-jan-21-in-rock-rapids-provides-essential-management-tips/",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 10
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.iowacorn.org/about/news/icpb-hosts-virtual-meetings-with-mexican-and-southeast-asian-trade-teams/",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Yesterday, the Iowa Corn Promotion Board® (ICPB) along with the U.S. Grains Council hosted three virtual trade team meetings with representatives from Mexico and Southeast Asia, including Malaysia, Cambodia, Lao, Myanmar and the Philippines. During their virtual meetings, the diverse groups learned about corn and corn co-products and the condition of this year’s crop from Iowa farmers. “I’ve been farming for 40 years and one of my favorite aspects about farming is showing and explaining my operation to export buyers,” said ICPB director and farmer from Woodward, Iowa, Rod Pierce. “The virtual meeting environment did not stop the participants from engaging and learning about our products.” The three separate meetings were held at various times on Thursday, October 15, and were arranged as part of the U.S. Grains Council’s Virtual Grain Exchange event. The topics ranged from this year’s growing season, corn quality and crop conditions, to grain handling, dried distillers grains (DDGS) and white corn production. Representatives also met with ICPB Industry Liaison Ryan Franklin, a Senior Merchandiser with Consolidated Grain and Barge (CGB) to discuss grain handling and corn quality. “Even though trade teams are virtual this year, the fact remains that all end-users want to get a good look at the entire U.S. agricultural value chain when making decisions about U.S. grains,” said Ryan LeGrand, U.S. Grains Council president and CEO. “The teams visiting Iowa are eager to not only see the state of corn harvest there, but also are keenly interested in getting a peek inside major production facilities so they can see for themselves just how high-quality Iowa corn is. By allowing them to do so, we can strengthen the relationships between U.S. farmers and these buyers, and we appreciate Iowa Corn’s assistance in this process.” “ICPB proudly invests checkoff dollars in the U.S. Grains Council to protect and expand markets for corn products around the world,” said ICPB President and farmer from Independence, Iowa, Greg Alber. “In this more socially distanced world, these meetings with current or prospective customers are more important than ever in strengthening global relationships, answering questions and further expanding corn demand internationally.” Brandi Snyder, Public Relations Manager, bsnyder@iowacorn.org , 515-225-9242"
    )
    assert r["created_at"] == "2020-10-16T00:00:00+00:00"
    assert r["tags"] == ["corn", "article", "iowacorn.org"]
    assert r["title"] == "ICPB Hosts Virtual Meetings with Mexican and Southeast Asian Trade Teams"
