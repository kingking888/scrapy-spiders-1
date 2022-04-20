"""Test suit for SoybeansandcornSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.kycorn import KentuckycornSpider
import pytest


@pytest.fixture()
def spider():
    return KentuckycornSpider()


headers = headers(KentuckycornSpider.host_header)
headers["User-Agent"] = KentuckycornSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            KentuckycornSpider.url,
            headers,
            [
                "https://news.ca.uky.edu/article/uk-begins-farm-variable-rate-irrigation-research",
                "https://www.kycorn.org/news/2020/10/27/uk-fall-crop-protection-webinar-series-begins-in-november",
                "https://www.kygrains.info/s/2020-10-cornsoybean.pdf",
                "https://www.kycorn.org/news/2020/10/9/biofuels-infrastructure-grants-to-boost-e15-pumps-at-kentucky-retail-locations",
                "https://kentuckypestnews.wordpress.com/2020/10/06/covid-commercial-applicators-ceus-and-epa-opportunities/",
                "https://www.kycorn.org/news/2020/10/2/corn-grower-investment-in-agriculture-literacy-amplified-through-partnerships",
                "https://www.usda.gov/media/blog/2020/09/24/americas-farmers-resilient-throughout-covid-pandemic",
                "https://www.kycorn.org/news/2020/9/25/next-generation-fuels-act-introduced",
                "https://www.kycorn.org/news/2020/9/25/investments-that-move-corn",
                "https://www.kycorn.org/news/2020/9/21/epa-announces-interim-decision-on-crucial-crop-protection-tools",
                "https://graincrops.ca.uky.edu/files/cornsoynewsletter2020vol2_iss4_sep.pdf",
                "https://graincrops.ca.uky.edu/files/cornsoynewsletter2020vol2_iss3_aug_0.pdf",
                "https://kentuckypestnews.wordpress.com/2020/08/18/spotted-corn-leaves-disease-or-something-different/",
                "https://www.kycorn.org/news/2020/8/14/kycorn-partners-with-caseys-general-store-for-e15-and-e85-pump-conversions",
                "https://www.kycorn.org/news/2020/8/14/core-program-connects-young-farmers-with-association-leaders",
                "https://www.kycorn.org/corn-yield-contest",
                "https://www.kycorn.org/news/2020/8/5/purchase-a-fields-of-corn-calendar-to-support-the-cornpac",
                "https://www.kycorn.org/news/2020/8/5/ncga-releases-mid-year-report-for-2020",
                "https://www.kycorn.org/news?offset=1596640847862",
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
            "https://www.kycorn.org/news?offset=1482869106000",
            headers,
            [
                "https://www.kycorn.org/news/2016/12/19/2016-national-corn-yield-contest-results",
                "https://www.kycorn.org/news/2016/12/5/core-farmer-program-class-iv-opens-with-farmer-advice",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.kycorn.org/news/2020/4/20/usda-announces-coronavirus-food-assistance-program",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "U.S. Secretary of Agriculture Sonny Perdue today announced the Coronavirus Food Assistance Program (CFAP). This new U.S. Department of Agriculture (USDA) program will take several actions to assist farmers, ranchers, and consumers in response to the COVID-19 national emergency. President Trump directed USDA to craft this $19 billion immediate relief program to provide critical support to our farmers and ranchers, maintain the integrity of our food supply chain, and ensure every American continues to receive and have access to the food they need. “During this time of national crisis, President Trump and USDA are standing with our farmers, ranchers, and all citizens to make sure they are taken care of,” Secretary Perdue said. “The American food supply chain had to adapt, and it remains safe, secure, and strong, and we all know that starts with America’s farmers and ranchers. This program will not only provide immediate relief for our farmers and ranchers, but it will also allow for the purchase and distribution of our agricultural abundance to help our fellow Americans in need.” CFAP will use the funding and authorities provided in the Coronavirus Aid, Relief, and Economic Security Act (CARES), the Families First Coronavirus Response Act (FFCRA), and other USDA existing authorities. The program includes two major elements to achieve these goals. 1. The program will provide $16 billion in direct support based on actual losses for agricultural producers where prices and market supply chains have been impacted and will assist producers with additional adjustment and marketing costs resulting from lost demand and short-term oversupply for the 2020 marketing year caused by COVID-19. 2. USDA will partner with regional and local distributors, whose workforce has been significantly impacted by the closure of many restaurants, hotels, and other food service entities, to purchase $3 billion in fresh produce, dairy, and meat. We will begin with the procurement of an estimated $100 million per month in fresh fruits and vegetables, $100 million per month in a variety of dairy products, and $100 million per month in meat products. The distributors and wholesalers will then provide a pre-approved box of fresh produce, dairy, and meat products to food banks, community and faith based organizations, and other non-profits serving Americans in need. On top of these targeted programs USDA will utilize other available funding sources to purchase and distribute food to those in need. Further details regarding eligibility, rates, and other implementation will be released at a later date. For all the information on USDA’s work during the COVID-19 pandemic and resources available, please visit . KyCorn President Richard Preston was interviewed regarding CFAP by Farms.com:"
    )
    assert r["created_at"] == "2020-04-20T00:00:00+00:00"
    assert r["tags"] == ["corn", "article", "kycorn.org"]
    assert r["title"] == "USDA Announces Coronavirus Food Assistance Program"
