"""Test suit for Waitr Investor Page."""

from agblox.spiders.helpers import headers
from agblox.spiders.waitr import WaitrInvestorsSpider
import pytest


@pytest.fixture()
def spider():
    return WaitrInvestorsSpider()


header_dict = headers(WaitrInvestorsSpider.host_header)
header_dict["User-Agent"] = WaitrInvestorsSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            WaitrInvestorsSpider.url,
            header_dict,
            [
                "http://investors.waitrapp.com/news-releases/news-release-details/waitr-reports-third-quarter-2020-results",
                "http://investors.waitrapp.com/news-releases/news-release-details/waitr-host-third-quarter-2020-earnings-conference-call-november",
                "http://investors.waitrapp.com/news-releases/news-release-details/waitr-adds-dine-capabilities-platform",
                "http://investors.waitrapp.com/news-releases/news-release-details/waitr-reports-second-quarter-2020-results",
                "http://investors.waitrapp.com/news-releases/news-release-details/waitr-completes-its-market-common-stock-offering",
                "http://investors.waitrapp.com/news-releases/news-release-details/waitr-announces-management-appointments",
                "http://investors.waitrapp.com/news-releases/news-release-details/waitr-pre-announces-second-quarter-2020-results",
                "http://investors.waitrapp.com/news-releases/news-release-details/waitr-expands-service-team-louisiana",
                "http://investors.waitrapp.com/news-releases/news-release-details/mats-diedrichsen-joins-waitr-advisor",
                "http://investors.waitrapp.com/news-releases/news-release-details/waitr-holdings-inc-announces-2020-annual-meeting-stockholders-be",
                "http://investors.waitrapp.com/news-events/news-releases?a9d908dd_year%5Bvalue%5D=_none&page=1",
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
            "http://investors.waitrapp.com/news-events/news-releases?a9d908dd_year%5Bvalue%5D=_none&page=6",
            header_dict,
            [
                "http://investors.waitrapp.com/news-releases/news-release-details/landcadia-holdings-inc-announces-separate-trading-its-class",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "http://investors.waitrapp.com/news-releases/news-release-details/five-guys-latest-partner-waitr",
            header_dict,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["url"]
        == "http://investors.waitrapp.com/news-releases/news-release-details/five-guys-latest-partner-waitr"
    )
    assert r["text"] == (
        "PDF Version\nLAFAYETTE, La. --(BUSINESS WIRE)--May 26, 2020--\nWaitr "
        "Holdings Inc. (Nasdaq: WTRH) (“Waitr” or the “Company”), a leader in "
        "on-demand food ordering and delivery, today announced a new partnership "
        "with Five Guys as it expands its delivery selection for diners. Effective "
        "immediately, customers using the Waitr app can order their favorite foods "
        "from more than 150 Five Guys locations around the nation.\n“We know, "
        "especially now, our customers are looking to us to deliver their favorite "
        "meals from a wider variety of restaurants. Adding the Five Guys brand to "
        "Waitr is an example of how we are meeting their requests,” said Carl "
        "Grimstad , CEO and Chairman of the Board at Waitr . “I love eating at Five "
        "Guys and now I can have it delivered to my home.”\nOver the past "
        "several weeks, Waitr has announced it is delivering same-day groceries; "
        "offering No-Contact delivery for all restaurant and grocery orders; "
        "working with restaurant partners to waive customer delivery fees; "
        "deploying free restaurant marketing programs, taking donations to feed the "
        "hungry, and providing gloves, masks and sanitation spray to drivers. The "
        "company has also committed to paying any employee who gets quarantined or "
        "contracts the virus.\nAbout Waitr Holdings Inc.\nFounded in 2013 "
        "and based in Lafayette, Louisiana , Waitr is a leader in on-demand food "
        "ordering and delivery. Waitr , and its sister brand Bite Squad, connects "
        "local restaurants and grocery stores to hungry diners in underserved U.S. "
        "markets. Together they are a convenient way to discover, order and receive "
        "great food from local restaurants, grocery stores and national chains. As "
        "of March 31, 2020 , Waitr and Bite Squad operated in small and medium "
        "sized markets in the United States in over 600 cities.\nView source "
        "version on businesswire.com : "
        "https://www.businesswire.com/news/home/20200526005235/en/\nInvestors\n"
        "WaitrIR@icrinc.com\nSource: Waitr Holdings Inc."
    )

    assert r["created_at"] == "2020-05-26T00:00:00+00:00"
    assert r["title"] == "Five Guys Latest to Partner with Waitr"
