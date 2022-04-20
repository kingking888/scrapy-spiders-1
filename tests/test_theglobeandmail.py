"""Test suit for TheGlobeAndMail spider."""
from agblox.spiders.globeandmail import GlobeAndMailSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return GlobeAndMailSpider()


@pytest.fixture()
def test_kwargs():
    return {"ticker": "FSR", "last_url": None}


headers = headers(GlobeAndMailSpider.host_header)
headers["User-Agent"] = GlobeAndMailSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.theglobeandmail.com/investing/markets/stocks/FSR-N/pressreleases/630205/",
            headers,
        ),
    ],
)
def test_created_at(spider, response, test_kwargs):
    r = next(spider.parse_article(response, **test_kwargs))
    assert r["created_at"] == "2021-11-13T00:00:00+00:00"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.theglobeandmail.com/investing/markets/stocks/TWTR-N/pressreleases/930908/",
            headers,
        ),
    ],
)
def test_created_at_two(spider, response, test_kwargs):
    r = next(spider.parse_article(response, **test_kwargs))
    assert r["created_at"] == "2022-01-11T00:00:00+00:00"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.theglobeandmail.com/investing/markets/stocks/FSR-N/pressreleases/475441/",
            headers,
        ),
    ],
)
def test_text_ony(spider, response, test_kwargs):
    r = next(spider.parse_article(response, **test_kwargs))
    assert r["text"] == (
        "Fisker Inc. (Fisker) - designer and manufacturer of the world's most emotion-stirring, "
        "eco-friendly electric vehicles and advanced mobility solutions - today announced the "
        "signing of a vehicle order for 300 units with Viggo, the technology-driven Danish ride-hailing "
        "service. Viggo, founded in 2019, is aiming to challenge the standards for urban transportation "
        "through advanced data-driven innovation, zero-emission cars and Scandinavian simplicity. "
        "Since founding, Viggo has built a network of more than 55 (100 projected by the end of"
        " the year) electric cars and delivered more than 100,000 rides. The company will expand "
        "into Norway in 2021 and the 300 Fisker Ocean all-electric luxury SUVs, to be delivered "
        "Q4 2022, will be a strong part of their Scandinavian expansion. Viggo's focus is on"
        " business users and has brought many large multinational companies into its customer/user"
        ' base. "We created the Fisker Ocean with space, range and value as product priorities,'
        ' attributes that are also very important to Viggo, their drivers and customers," said '
        'Henrik Fisker, chairman and CEO of Fisker. "As someone born and raised in Denmark, I am'
        " also personally proud that this Danish company has chosen to work with Fisker and put "
        "their confidence in our company and products. This agreement is the first of many multi-vehicle"
        " orders that we are planning to sign with both mobility companies like Viggo and large "
        'corporate fleets." Fisker recently announced a strategic cooperation with Magna International'
        " supporting the co-development and manufacture of the Fisker Ocean SUV, projected to"
        " launch in Q4 2022. The Ocean will be assembled by Magna in Europe and is poised to "
        "deliver class-leading range, functional interior space with third-row seating and overall"
        " vehicle performance. On behalf of Viggo, CEO Kenneth Herschel and Chairman Peter "
        'Bardenfleth-Hansen made the following comment: "We founded Viggo to create a better'
        " and more sustainable experience all-around for our customers, and so our choice of"
        " vehicle is a critically important part of that service delivery. The seating and "
        "flexible space of the Fisker Ocean, together with the projected cost of operation, makes"
        ' this vehicle a very logical choice for our fleet." For more information, or for interview '
        "inquiries, contact Fisker@GoDRIVEN360.com. About Fisker Inc. California-based Fisker Inc."
        " is revolutionizing the automotive industry by developing the most emotionally desirable"
        " and eco-friendly electric vehicles on Earth. Passionately driven by a vision of a clean"
        " future for all, the company is on a mission to become the No. 1 e-mobility service "
        "provider with the world's most sustainable vehicles. To learn more, visit www.FiskerInc.com "
        "- and enjoy exclusive content across Fisker's social media channels: Facebook, Instagram,"
        " Twitter, YouTube and LinkedIn. Download the revolutionary new Fisker mobile app from the App"
        " Store or Google Play store. About Viggo HQ ApS Viggo is a Danish technology company driving"
        " the green change with climate-friendly mobility in the city. With advanced data-driven innovation,"
        " zero-emission cars, and Scandinavian simplicity, Viggo will revolutionize the way we move. The goal "
        "is to challenge the standards for urban transportation. Customer feedback is critical input for service"
        " development and the experiences are rated directly in the app for service and safety. Read more at "
        "www.viggo.com. View source version on "
        "businesswire.com: https://www.businesswire.com/news/home/20201021005384/en/"
        ' SOURCE: Fisker Inc.">'
    )


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.theglobeandmail.com/investing/markets/stocks/FSR-N/pressreleases/491467/",
            headers,
        ),
    ],
)
def test_article(spider, response, test_kwargs):
    r = next(spider.parse_article(response, **test_kwargs))
    assert r["text"] == (
        "Fisker Inc. (Fisker) - designer and manufacturer of the world's most emotion-stirring, "
        "eco-friendly electric vehicles and advanced mobility solutions - today announced that "
        "it is set to reveal the production version of the Fisker Ocean, its all-electric SUV,"
        " at the 2021 Los Angeles Auto Show. This press release features multimedia. View the "
        "full release here: https://www.businesswire.com/news/home/20201023005115/en/ Fisker "
        "recently announced a strategic cooperation with Magna International supporting the "
        "co-development and manufacture of the Fisker Ocean SUV, projected to launch in Q4 2022."
        " The Ocean will be assembled by Magna in Europe and is poised to deliver class-leading "
        "range, functional interior space with third-row seating and overall vehicle performance. "
        "Earlier this week, Fisker also confirmed the signing of a significant vehicle order for "
        "300 units with Viggo, the technology-driven Danish ride-hailing service. Viggo, founded "
        "in 2019, is aiming to challenge the standards for urban transportation through advanced"
        " data-driven innovation delivered through a fleet of 100% electric vehicles. Henrik Fisker,"
        " chairman and chief executive officer of Fisker, stated, \"It's with great excitement"
        " that we're making the global debut of the Fisker Ocean here in our home city of Los"
        " Angeles. As befits the world's first digital car company, we are also planning to "
        "showcase several Fisker-unique technologies that will support our differentiated ownership"
        ' experience and vehicle functionality." Following the cancellation of the 2020 Los Angeles'
        " Auto Show, Fisker made the strategic decision to commit to the 2021 show for the global "
        "reveal of the Ocean SUV, its first production vehicle. The 2021 Los Angeles Auto Show will "
        "run from May 21-31 at the LA Convention Center. Originally founded in Los Angeles, Fisker "
        "recently announced details surrounding its new global HQ, named 'Inception,' which is to be"
        " located within Continental Park at 1888 Rosecrans Avenue in the city of Manhattan Beach. "
        "For more information, or for interview inquiries, contact Fisker@GoDRIVEN360.com. About Fisker"
        " Inc. California-based Fisker Inc. is revolutionizing the automotive industry by developing "
        "the most emotionally desirable and eco-friendly electric vehicles on Earth. Passionately driven"
        " by a vision of a clean future for all, the company is on a mission to become the No. 1 "
        "e-mobility service provider with the world's most sustainable vehicles. To learn more, visit"
        " www.FiskerInc.com - and enjoy exclusive content across Fisker's social media channels: "
        "Facebook, Instagram, Twitter, YouTube and LinkedIn. Download the revolutionary new Fisker "
        "mobile app from the App Store or Google Play store. View source version on businesswire.com: "
        'https://www.businesswire.com/news/home/20201023005115/en/ SOURCE: Fisker Inc.">'
    )
    assert r["created_at"] == "2021-10-23T00:00:00+00:00"
    assert r["tags"] == ["equity", "globeandmail", "article", "FSR"]
    assert (
        r["title"]
        == "Fisker Inc. Set to Reveal Production Ocean SUV at the Los Angeles Auto Show, May 2021"
    )
