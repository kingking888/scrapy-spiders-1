"""Test suit for TexasCornSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.texascorn import TexasCornSpider
import pytest


@pytest.fixture()
def spider():
    return TexasCornSpider()


headers = headers(TexasCornSpider.name)
headers["User-Agent"] = TexasCornSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            TexasCornSpider.url,
            headers,
            [
                "https://texascorn.org/make-an-informed-vote-tcpa-voter-guide/",
                "https://texascorn.org/investing-in-our-educators/",
                "https://texascorn.org/texas-corn-farmers-to-take-national-appointments-3/",
                "https://texascorn.org/cfap-2-assistance-welcomed-by-farmers-hard-hit-in-2020/",
                "https://texascorn.org/harvest-covid-19-underscore-need-for-farm-readiness/",
                "https://texascorn.org/corn-conversations-expanding-markets/",
                "https://texascorn.org/texas-producers-grow-through-ncgas-leadership-training/",
                "https://texascorn.org/texas-producer-attends-national-leadership-conference/",
                "https://texascorn.org/tcpa-visits-with-congressional-candidate/",
                "https://texascorn.org/association-attends-presidential-visit-to-texas/",
                "https://texascorn.org/ring-recognized-for-support-contributions-to-agriculture/",
                "https://texascorn.org/insect-resistance-management-assessment-notice/",
                "https://texascorn.org/page/2/?s&id=1&post_type=post",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 13
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://texascorn.org/page/6/?s&id=1&post_type=post",
            headers,
            [
                "https://texascorn.org/2017-farm-program-payments-announced-arc-county-rates-widely-variable-in-texas/",
                "https://texascorn.org/texas-corn-farmers-to-take-national-appointments/",
                "https://texascorn.org/tcpa-submits-comments-to-epa-on-2019-rvo/",
                "https://texascorn.org/tcpb-to-hold-2018-biennial-election/",
                "https://texascorn.org/statement-on-the-governors-renewable-fuels-standard-waiver-request/",
                "https://texascorn.org/tcpb-announces-biennial-elections-for-five-seats/",
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
            "https://texascorn.org/tcpa-submits-comments-to-epa-on-2019-rvo/",
            headers,
        ),
    ],
)
def test_created_at(spider, response):
    r = next(spider.parse_article(response))
    assert r["created_at"] == "2018-08-17T00:00:00+00:00"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://texascorn.org/funding-the-future/",
            headers,
        ),
    ],
)
def test_text_ony(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == """Texas Corn Producers (TCP) believes in investing in the future of agriculture through multiple avenues to ensure today’s youth is educated and informed. In order to further this mission, TCP is proud to announce its 2019 scholarship recipients!\nThis year’s applicant pool was as competitive as ever and TCP was pleased to receive a variety of eligible, well deserving applicants. In total, four youth members were chosen to receive a $1,000 scholarship within two categories.\nIn the high school division, Preston Dallmeyer, of Poth, Texas, is one of two winners. Preston wrote about the effects of aflatoxin on corn yields. Preston is planning on attending Texas Tech University where he will study architecture.\nClara Steglich, of Holland, Texas, joined in as a winner in the high school division. Clara wrote about the struggles farmers face with GMO marketing. Clara is currently attending Texas A&M University studying agricultural science.\nIn the collegiate division, Kendall Stone, of Caldwell, Texas, was awarded a scholarship with an essay about the environmental and economic factors farmers face. Kendall is currently studying agriculture science at Texas A&M.\nSavannah Wesley, of Tulia, Texas, received a collegiate scholarship with her essay concerning water policy. Savannah is currently studying broadcast journalism at West Texas A&M University.\nHannah Dast, the TCP education director said,\n“TCP values the opportunity to invest in the future of our industry through scholarships for our youth. We had an impressive set of applicants this year and look forward to what they will accomplish during their college careers and beyond.”\nTCP is grateful for all who applied to and promoted the youth scholarship program and we are excited to receive applications for the 2020 scholarship.\nFor those who are interested in the 2020 scholarship application, visit texascorn.org/scholarships"""
    )


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://texascorn.org/texas-corn-farmers-to-take-national-appointments-3/",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Four Texas corn farmers are set to take on key advising positions for "
        "National Corn Growers Association (NCGA) in 2021. Earlier this week, "
        "the NCGA Corn Board appointed farmer and staff leaders from across the "
        "nation to its action teams and committees.\n“Having a voice at this "
        "level is vital to ensuring a diverse perspective as national efforts are "
        "driven by these action teams and committees,” Texas Corn Producers Board "
        "Chairman Robert Gordon said. “Committing time away from the farm is never "
        "easy, and the dedication of these Texans will prove beneficial to the corn "
        "industry as a whole.”\nThe NCGA Corn Board selected farmers for a "
        "variety of positions:\nKyla Hamilton of Shallowater, Texas\nMember "
        "and Consumer Engagement Action Team\nAaron Martinka of Buckholts, "
        "Texas\nRisk Management and Transportation Action Team\nCharles Ring of "
        "Sinton, Texas\nSustainability Ag Research Action Team\nChad Wetzel of "
        "Sherman, Texas\nStewardship Action Team\n“We look forward to seeing "
        "the leadership of these individuals alongside fellow corn farmers from "
        "across the nation grow the industry over the next year,” Texas Corn "
        "Producers Association President Wesley Spurlock said. “It’s important to "
        "have a Texan perspective brought into the conversation of the teams that "
        "guide core programs for the organization’s policies and priorities.”\n"
        "NCGA relies on a strong group of farmer leaders for the organization to "
        "thrive and serve its purpose as a nationwide representation of one of the "
        "largest agricultural segments of the United States. Access the complete "
        "list of NCGA action team and committee appointments HERE ."
    )

    assert r["created_at"] == "2020-10-09T00:00:00+00:00"
    assert r["tags"] == ["article", "texascorn.org"]
    assert r["title"] == "Texas corn farmers to take national appointments"
