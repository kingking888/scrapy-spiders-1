"""Test suit for SoyGrowers."""

from agblox.spiders.helpers import headers
from agblox.spiders.soy_growers import SoyGrowersSpider
import pytest


@pytest.fixture()
def spider():
    return SoyGrowersSpider()


headers = headers(SoyGrowersSpider.name)
headers["User-Agent"] = SoyGrowersSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            SoyGrowersSpider.url,
            headers,
            [
                "https://soygrowers.com/news-releases/new-cambodian-aquaculturist-association-catches-national-media-coverage/",
                "https://soygrowers.com/news-releases/soy-growers-appreciate-dicamba-to-remain-weed-control-option/",
                "https://soygrowers.com/news-releases/wishh-releases-mini-documentary-on-inspiring-entrepreneurs-insights-for-protein-progress/",
                "https://soygrowers.com/news-releases/wishh-will-put-soy-on-center-stage-in-aquafeeds-in-africa-webinar/",
                "https://soygrowers.com/news-releases/american-soybean-association-seeks-candidates-for-soy-scholarship-4/",
                "https://soygrowers.com/news-releases/seesoyharvest/",
                "https://soygrowers.com/news-releases/so-nice-hes-doing-it-twice-censky-returning-to-soy/",
                "https://soygrowers.com/news-releases/wishhworks-campaign-wrap-ag-radio-tv-successfully-spotlight-wishhs-trade-development-work/",
                "https://soygrowers.com/news-releases/asa-and-usb-partner-to-provide-educational-webinar-on-rural-broadband-challenges/",
                "https://soygrowers.com/news-releases/asa-5-big-reasons-why-wishhs-work-matters-right-now/",
                "https://soygrowers.com/news-media/news-releases/page/2/",
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
            "https://soygrowers.com/news-media/news-releases/page/11/",
            headers,
            [
                "https://soygrowers.com/news-releases/resources-for-farmers-to-besure-about-best-stewardship-practices-this-spring/",
                "https://soygrowers.com/news-releases/eus-exclusion-of-agriculture-disappointing-for-soy-growers/",
                "https://soygrowers.com/news-releases/biodiesel-tax-credit-marker-bill-introduced-house-supporters-push-leadership-to-act/",
                "https://soygrowers.com/news-releases/u-s-soy-leaders-promote-u-s-soy-advantage-on-china-tour/",
                "https://soygrowers.com/news-releases/cambodian-animal-feed-millers-receive-technical-assistance/",
                "https://soygrowers.com/news-releases/soybean-growers-unhappy-with-president-trumps-comments-on-keeping-tariffs-in-place-under-a-china-agreement/",
                "https://soygrowers.com/news-releases/wishh-highlights-importance-of-soy-on-international-school-meals-day/",
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
            "https://soygrowers.com/news-releases/36th-young-leader-class-kicks-off-in-indianapolis/",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == """Washington, D.C. Jan. 7, 2020. The 36th class of American Soybean Association (ASA) Corteva Agriscience Young Leaders recently began its leadership journey at the Corteva Agriscience Global Business Center in Indianapolis, Indiana. The Indianapolis training session was the first phase of the program designed to identify future grower leaders within the agriculture community and provide them with opportunities to enhance their skills and network with other farmers. Representatives from 19 states and the Grain Farmers of Ontario participated in the program. During the training, ASA President Bill Gordon (MN) provided participants with an association overview and United Soybean Board (USB) Director Mark Seib discussed the checkoff and engagement of future agricultural leaders. ASA Vice President Kevin Scott (SD) joined the program via teleconference for a panel discussion and open forum on the soybean industry. The Young Leaders also participated in leadership styles and communications training, discussed consumer trends and acceptance, and were introduced to AgriNovus Indiana. Additional discussion provided updates on other soybean industry advancements. “As a graduate of the Young Leader program, I’ve seen firsthand how this training provides participants with the tools and knowledge they need to be an effective advocate for agriculture,” Gordon said. “Former Young Leaders can be found in leadership roles throughout the industry and public policy. We are grateful to Corteva Agriscience for making this program possible and helping to lay the foundation of agriculture’s future.” “Corteva Agriscience was proud to welcome the ASA Corteva Agriscience™ Young Leaders to Indianapolis, Indiana for the first time in our 36-year history as the program sponsor,” said Susanne Wasson, President, Crop Protection Business Platform, Corteva Agriscience. “The Young Leader Program provides participants developmental training to hone their leadership skills and strengthen the voice of agriculture. After meeting with the 2019-2020 Young Leader participants, I am confident the future of the soybean industry is in good hands.” The 2020 Young Leaders are: Caper & Alison Robinson (AR); Jesse Patrick (GA); Brady Holst (IL); James Ramsey (IN); Eric Schwenke (IN); Noah & Anna Fedders (IA); Ryan & Kristin Oberbroeckling (IA); Jeremy Olson (KS); Houston & Kathryn (Katy) Howlett (KY); Nathan Engelhard (MI): Allison Morse (MI); Mike & Dawn Kunerth (MN); Ryan Mackenthun (MN); Garrett & Cara Riekhof (MO); Josh England (NE); Lucas & Becky Miller (NE); Trey & Rebecca Liverman (NC); Justin Sherlock (ND); Justin & Emily Esselburn (OH); Scott Ruck (OH); Jesse & Emily King (SD); Drew Peterson (SD); Casey Youngerman (TN); Adam & Brittany Davis (VA); Matt Rehberg (WI); Chris & Rachel Renwick (Canada). This second phase of the Young Leader program will take place Feb. 25 – 29, 2020 in San Antonio, Texas, with training held in conjunction with the annual Commodity Classic Convention and Trade Show."""
    )
    assert r["created_at"] == "2020-01-07T00:00:00+00:00"
    assert r["tags"] == ["soy", "article", "soygrowers.com"]
    assert r["title"] == "36th Young Leader Class Kicks Off in Indianapolis"
