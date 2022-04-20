"""Test suit for AgfaxSpider."""

from agblox.spiders.agriculturecom.soybeans import AgriculturecomSoybeansSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return AgriculturecomSoybeansSpider()


@pytest.fixture()
def last_page_spider():
    s = AgriculturecomSoybeansSpider()
    s.first_page = False
    return s


headers = headers(AgriculturecomSoybeansSpider.host_header)
headers["User-Agent"] = AgriculturecomSoybeansSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            AgriculturecomSoybeansSpider.url,
            headers,
            [
                "https://www.agriculture.com/crops/corn/new-tech-coming-in-seed-traits",
                "https://www.agriculture.com/crops/soybeans/why-soybean-farmers-need-to-manage-soybean-cyst-nematode",
                "https://www.agriculture.com/podcast/successful-farming-radio-podcast/soybean-seeding-rates",
                "https://www.agriculture.com/crops/soybeans/all-about-adjuvants",
                "https://www.agriculture.com/podcast/successful-farming-radio-podcast/advances-in-soybean-breeding",
                "https://www.agriculture.com/podcast/successful-farming-podcast/preventing-soybean-loss-during-harvest",
                "https://www.agriculture.com/crops/soybeans/reevaluate-your-soybean-strategy-for-2021",
                "https://www.agriculture.com/podcast/successful-farming-radio-podcast/soybean-row-spacing",
                "https://www.agriculture.com/crops/soybeans/soil-testing-keys-successful-soybean-cyst-nematode-management",
                "https://www.agriculture.com/crops/soybeans?page=1",
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
            "https://www.agriculture.com/crops/soybeans?page=106",
            headers,
            [
                "https://www.agriculture.com/crops/soybeans/production/Expert-predicts-low-soybean-aphid-numbers-in-Ohio_141-ar157",
                "https://www.agriculture.com/crops/soybeans/production/High-Yield-Team-Whats-happening-with-the-miracle-crop_141-ar86",
                "https://www.agriculture.com/crops/soybeans/production/High-Yield-Team-shoots-to-boost-bean-yields-by-30-on-challenged-fields_141-ar83",
            ],
        ),
    ],
)
def test_last_page(last_page_spider, response, expected):
    r = [e.url for e in last_page_spider.parse(response)]
    print(r)
    assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.agriculture.com/crops/soybeans/why-soybean-farmers-need-to-manage-soybean-cyst-nematode",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "The number one yield-grabbing pest for soybeans is one farmers cannot visually see. Left "
        "unmanaged, soybean cyst nematode (SCN) can significantly impact their bottom "
        "lines.\nThat’s why the Soybean Cyst Nematode Coalition--a public/checkoff/private "
        "partnership formed to increase the number of farmers who are actively managing "
        "SCN--recommends that soybean growers work with an expert to develop a plan to actively "
        "manage SCN.\nGreg Tylka, an Iowa State University nematologist, says SCN is "
        "considered to be the most damaging pathogen, in part, because the most common source of "
        "resistance known as PI 88788 isn’t as effective as it once was.\n“SCN thrives in the "
        "soil and takes food away from the soybean plant,” he says. “It’s also widely distributed "
        "and continues to spread where soybeans are grown.”\nIn a new video series titled "
        "“Let’s Talk Todes,” Tylka explains why soybean growers need to consider the economic "
        "impacts of SCN.\n“Don’t be complacent,” he says. “The nematode doesn’t actively "
        "spread itself; it’s spread by anything that moves soil. It’s spreading within states "
        "where it’s well established like Iowa and Illinois, and more recently moved into areas "
        "of the Upper Midwest like North Dakota.”\nSam Markell, a North Dakota State "
        "University plant pathologist, encourages growers to test for SCN so its spread can be "
        "tracked.\n“If we find it, we need to manage it, and we can learn from the situation "
        "in states like Iowa,” he says. “Growers will benefit by incorporating varieties with the "
        "Peking source of SCN resistance into their rotation. This can translate into yield "
        "benefits in areas where PI 88788 is not as effective, and rotation between these two "
        "sources of resistance can help keep the nematode from overcoming PI 88788 in new areas. "
        "Early detection, frequent monitoring and strategic management are keys to managing the "
        "number one yield-grabbing pest of the soybean crop in North America.”"
    )
    assert r["created_at"] == "2020-11-16T00:00:00+00:00"
    assert r["title"] == "Why soybean farmers need to manage soybean cyst nematode"
