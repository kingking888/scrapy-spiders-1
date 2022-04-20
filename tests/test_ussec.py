"""Test suit for TexasCornSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.ussec import UssecSpider
import pytest


@pytest.fixture()
def spider():
    return UssecSpider()


headers = headers(UssecSpider.name)
headers["User-Agent"] = UssecSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            UssecSpider.url,
            headers,
            [
                "https://ussec.org/opportunities-for-u-s-soy-in-sub-saharan-africa-livestock-feed/",
                "https://ussec.org/ussec-launches-new-global-marketing-campaign/",
                "https://ussec.org/russian-feed-industry-learns-more-about-u-s-soy-fermented-soybean-meal-at-mixed-feeds-2020-international-conference/",
                "https://ussec.org/ussec-bridges-the-gap-between-u-s-soybean-oil-and-colombian-refineries/",
                "https://ussec.org/microscopy-helps-feed-mills-with-quality-control/",
                "https://ussec.org/ussec-promotes-two-within-its-ranks/",
                "https://ussec.org/polish-dairy-stakeholders-explore-the-advantage-of-u-s-soy-in-livestock-diets/",
                "https://ussec.org/analyzing-the-global-soybean-complex/",
                "https://ussec.org/novelties-key-knowledge-gaps-in-soy-feed-ingredient-quality-control/",
                "https://ussec.org/soy-news/page/2/",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 10
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://ussec.org/soy-news/page/245/",
            headers,
            [
                "https://ussec.org/chinese-commit-to-record-setting-u-s-soybeans-deals-during-ussecarranged-visits-to-iowa-los-angeles/",
                "https://ussec.org/chairmans-report-february-23-2012/",
                "https://ussec.org/special-news-edition-global-news-update-february-17-2012/",
                "https://ussec.org/global-news-update-december-10-2012/",
                "https://ussec.org/global-news-update-october-22-2010/",
                "https://ussec.org/november-2008/",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 6
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://ussec.org/ussec-mourns-dwain-ford/",
            headers,
        ),
    ],
)
def test_created_at(spider, response):
    r = next(spider.parse_article(response))
    assert r["created_at"] == "2015-08-17T21:28:17-05:00"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://ussec.org/ussec-china-aquaculture-program-conducted-webinar-promote-ssap-bap/",
            headers,
        ),
    ],
)
def test_text_ony(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == """USSEC continues to leverage its virtual communications during the COVID-19 pandemic.\nOn April 9, USSEC’s China Aquaculture Program conducted its first webinar on the promotion of the U.S. Soy Sustainability Assurance Protocol (SSAP) and Best Aquaculture Practices (BAP). The team rented the platform from Fishfirst, one of the most influential aquaculture magazines in the country, to live-webcast this seminar. Statistics showed that the total page-viewer number reached over 45,000 while the number of participants to the webinar was over 1,000 (from Fishfirst). At the webinar, three speakers, including USSEC consultant David Li and the Global Aquaculture Aliance’s (GAA) Kevin Yuan and Jeff Yuan, gave presentations: introducing SSAP, the application procedures for BAP certification, and reviewing technical details on BAP requirements. Towards the end of the webinar, speakers answered participants’ questions and feedback from participants showed the satisfactory rate as very high. However, turn-in rate of surveys was lower than anticipated because previous Fishfirst customers had not asked the platform to provide this service, which resulted in poor webpage design for the survey. At the end of the webinar, only about 20 surveys were completed and turned in. USSEC talked to Fishfirst about this issue and Fishfirst promised to improve the survey capabilities for the next USSEC webinar.\nEver since the COVID-19 outbreak began, the Chinese aquaculture team has been confined to its home base for nearly three months with no capability of participating in meetings, conducting seminars, and visiting its target audience, which makes doing business virtually the only option. In the near future, this team plans to conduct two more webinars on the promotion of IPRS (In-Pond Raceway System). USSEC has been promoting IPRS in the country for more than seven years, winning the full recognition of both the industry and the Chinese government. The government announced early this month that IPRS will be one of the five top priority aquaculture technologies to be extended in the country in the future, and so the team anticipates the coming webinars will attract more participants. In the not-so-distant future, USSEC plans to do some webinars with pre-recordings from the consultants about the superior intrinsic value of U.S. Soy over soy from other origins for aquatic animals. The aquaculture team will share the data collected and analyzed from the past two years’ soy comparison lab study in China with the industry.\nThe advertising for the webinar\nScreenshot of David Li, USSEC China Aqua Webinar Advertising Program Assistant, speaking at the webinar\nShare This"""
    )


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://ussec.org/ussec-welcomes-senior-director-organizational-collaboration-innovation/",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Karey Claghorn has joined USSEC as Senior Director – Organizational Collaboration and "
        "Innovation. Ms. Claghorn was previously the Chief Operating Officer for the Iowa Soybean "
        "Association.\nThis new role focuses on increasing the organization’s "
        "effectiveness.\nCollaboration Leader – ensuring that best practices from regions, "
        "industries, etc. are implemented and utilized throughout USSEC, emphasizing on "
        "increasing uniformity and predictability.\nIncubation leader – to move new "
        "ideas/projects forward expeditiously.\nExecutive level oversight of:\nUnique, "
        "high profile programs such as the Protein Deficiency Program in India and centralized "
        "leadership for ATP Program.\nDirector of Strategic Program Development and Director of "
        "Measurement and Evaluation positions.\n“I’m very pleased we have the opportunity to "
        "bring an individual with Karey’s experience, skills, and dedication to U.S. Soy onto our "
        "great team,” states USSEC CEO Jim Sutter. “Please join me in welcoming Karey to her new "
        "role.”\nShare This"
    )
    assert r["created_at"] == "2019-11-12T21:01:38-06:00"
    assert r["tags"] == ["soy", "article", "ussec.org"]
    assert (
        r["title"]
        == "USSEC Welcomes Senior Director \u2013 Organizational Collaboration and Innovation"
    )
