"""Test suit for PurdueSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.ilcorn import IlcornSpider
import pytest


@pytest.fixture()
def spider():
    return IlcornSpider()


headers = headers(IlcornSpider.host_header)
headers["User-Agent"] = IlcornSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            IlcornSpider.url,
            headers,
            [
                "https://www.ilcorn.org/news-and-media/current-news/article/2020/11/korean-buyers-purchase-us-corn-after-illinois-meeting",
                "https://www.ilcorn.org/news-and-media/current-news/article/2020/10/dicamba-ruling-with-il-corn-board-director-randy-desutter",
                "https://www.ilcorn.org/news-and-media/current-news/article/2020/10/internal-combustion-engine-ban-could-devastate-agriculture",
                "https://www.ilcorn.org/news-and-media/current-news/article/2020/10/epa-approved-dicamba-products-for-use-through-2025",
                "https://www.ilcorn.org/news-and-media/current-news/article/2020/10/in-support-of-a-new-lock-and-dam-start-in-2021",
                "https://www.ilcorn.org/news-and-media/current-news/article/2020/10/audio-update-importance-of-the-lock-and-dam-system-with-marty-marr",
                "https://www.ilcorn.org/news-and-media/current-news/article/2020/10/lagrange-lock-on-the-illinois-river-reopens-other-newly-maintained-locks-follow",
                "https://www.ilcorn.org/news-and-media/current-news/article/2020/10/farmers-meet-with-mexican-and-korean-business-reps",
                "https://www.ilcorn.org/news-and-media/current-news/article/2020/10/audio-update-pcm-developments-with-travis-deppe",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert r[:9] == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.ilcorn.org/news-and-media/current-news/article/2020/09/epa-announced-interim-decision",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Today, the Environmental Protection Agency (EPA) announced a long-awaited interim decision regarding the reregistration of the triazines: atrazine, propazine, and simazine. After years of research and public comments from the agriculture community, EPA Administrator Andrew Wheeler declared these fundamental crop management tools safe for continued use in controlling resilient weeds. The interim decision is a major milestone for farmers who rely on atrazine to fight problematic weeks and employ conservation tillage methods to reduce soil erosion and improve water and wildlife habitat. on this issue, saying that, “Atrazine is critical for farmers who are using innovative conservation practices to minimize tillage on their farms. Because farmers have access to atrazine and can employ conservation tillage methods, they have lessened runoff of water, soil, nutrients, and pesticides, preventing erosion and protecting aquatic ecosystems and water quality. These methods also allow for a reduction in greenhouse gas emissions.” Atrazine ranks second in widely used herbicides that help farmers control weeds that rob crops of water and nutrients. Utilized for over 60 years, atrazine is the most researched herbicide in history and has a proven safety record. Today’s announcement concludes the registration review process where EPA is required to periodically re-evaluate existing pesticides under the Federal Insecticide, Fungicide, and Rodenticide Act (FIFRA). The next step for the triazines is a draft biological evaluation required under the Endangered Species Act (ESA), which is expected to be published in October. The EPA has committed to utilizing the best available research during this ESA evaluation. The ag community will again hold them to their intention by vigilantly pushing the high-quality, scientific studies on atrazine to the forefront for consideration. Approved for use 1958, atrazine has been extensively reviewed by EPA and others over the decades and across administrations. The final ESA assessment is slated to be released in 2021."
    )
    assert r["created_at"] == "2020-09-21T00:00:00+00:00"
    assert r["tags"] == ["article", "ilcorn.org"]
    assert r["title"] == "EPA Announces Interim Decision on Crucial Crop Protection Tools"
