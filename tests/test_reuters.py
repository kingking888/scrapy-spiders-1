"""Test suit for ReutersSpider."""
from agblox.spiders.helpers import headers
from agblox.spiders.reuters import ReutersSpider
import pytest


@pytest.fixture()
def spider():
    return ReutersSpider()


headers = headers(ReutersSpider.host_header)
headers["User-Agent"] = ReutersSpider.user_agent
del headers["Host"]


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            ReutersSpider.url,
            headers,
            [
                "https://www.reuters.com/article/indonesia-palmoil-biodiesel/indonesias-pertamina-conducts-trials-on-100-palm-oil-biodiesel-and-jet-fuel-idUSL4N2JQ0WO",
                "https://www.reuters.com/article/health-birdflu-asia/rpt-corrected-reeling-from-coronavirus-asias-poultry-farmers-battle-bird-flu-outbreak-idUSL1N2JQ03A",
                "https://www.reuters.com/article/health-coronavirus-france-winegrowers/french-winegrowers-hit-by-u-s-tariffs-will-get-extra-financial-aid-minister-idUSP6N2I9026",
                "https://www.reuters.com/article/us-usa-biofuels/u-s-epa-eyes-extending-refinery-biofuel-deadlines-no-action-on-waivers-idUSKBN29J226",
                "https://www.reuters.com/article/aphria-results/update-2-aphria-posts-quarterly-profit-on-cannabis-demand-shares-jump-idUSL4N2JP33L",
                "https://www.reuters.com/article/usa-china-companies/update-2-u-s-adds-cnooc-to-black-list-saying-it-helps-china-intimidate-neighbors-idUSL1N2JP1IO",
                "https://www.reuters.com/article/soufflet-ma-invivo/media-link-invivo-offered-nearly-2-3-bln-euros-to-take-over-soufflet-challenges-magazine-idUSL8N2JP4YD",
                "https://www.reuters.com/article/uk-safrica-landbank/s-africas-land-bank-reworking-debt-plan-after-state-guarantee-declined-idUSKBN29J201",
                "https://www.reuters.com/article/us-eu-agriculture-environment/eu-farmers-could-get-cash-to-curb-emissions-from-belching-livestock-idUSKBN29J213",
                "https://www.reuters.com/article/us-weather-lanina/la-nia-to-persist-until-march-says-u-s-weather-forecaster-idUSKBN29J1VD",
                "https://www.reuters.com/article/usa-china-companies/u-s-adds-cnooc-to-economic-black-list-idUSL8N2JP4JK",
                "https://www.reuters.com/article/us-usa-grains-braun/column-rising-new-crop-corn-soy-prices-intensify-u-s-acreage-duel-idUSKBN29J1V9",
                "https://www.reuters.com/article/us-hungary-bird-flu/hungary-orders-slaughter-of-101000-chickens-after-bird-flu-outbreak-idUSKBN29J1QC",
                "https://www.reuters.com/article/aphria-results/aphria-posts-quarterly-profit-on-cannabis-demand-during-lockdown-idUSL4N2JP2ZM",
                "https://www.reuters.com/article/us-asia-palmoil/planters-say-anti-palm-oil-campaigns-hinder-sustainability-shift-idUSKBN29J13M",
                "https://www.reuters.com/article/india-soymeal-exports/indias-soymeal-exports-could-more-than-double-as-prices-rally-idUSKBN29J13U",
                "https://www.reuters.com/article/health-birdflu-asia/corrected-reeling-from-coronavirus-asias-poultry-farmers-battle-bird-flu-outbreak-idUSL4N2JI1PF",
                "https://www.reuters.com/article/russia-inflation-health-coronavirus/russia-to-adjust-inflation-basket-for-demand-shifts-during-pandemic-idUSL8N2JP1KZ",
                "https://www.reuters.com/article/india-vegoils-imports/indias-december-palm-oil-imports-jump-4-on-duty-cut-trade-body-says-idUSKBN29J0V2",
                "https://www.reuters.com/article/china-economy-trade-meat/update-3-china-2020-meat-imports-close-to-10-mln-tonnes-up-60-on-year-idUSL1N2JP068",
                "https://wireapi.reuters.com/v7/feed/url/www.reuters.com/markets/agriculture?until=1610611426004645000",
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
            "https://wireapi.reuters.com/v7/feed/url/www.reuters.com/markets/agriculture?until=1578875185031204000",
            headers,
            [
                "https://www.reuters.com/article/usa-trade-china/chinas-u-s-trade-deal-commitments-not-changed-in-translation-mnuchin-idUSL1N29H05A",
                "https://wireapi.reuters.com/v7/feed/url/www.reuters.com/markets/agriculture?until=1578851845002256000",
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
            "https://www.reuters.com/article/china-economy-trade-meat/update-3-china-2020-meat-imports-close-to-10-mln-tonnes-up-60-on-year-idUSL1N2JP068",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "(Adds chart) BEIJING, Jan 14 (Reuters) - China imported 9.91 million tonnes "
        "of meat in 2020, customs data showed on Thursday, as the world’s biggest "
        "consumer of meat stocked up on proteins after a further plunge in its pork "
        "output. Shipments were up 60.4% on the year before and came after China’s "
        "output of pork, its staple meat, slumped 19% in the first half. That "
        "followed an even bigger drop during 2019 when the fatal pig disease African "
        "swine fever ravaged its vast hog herd. China’s General Administration of "
        "Customs only began releasing monthly data for all meats combined last year "
        "but the 2020 total is believed by industry analysts to be a record. “It’s "
        "definitely a record. All the species hit records last year,” said Pan "
        "Chenjun, senior analyst at Rabobank. Imports of pork from the United States, "
        "China’s largest supplier, rose 223.8% in yuan terms in 2020, customs "
        "spokesman Liu Kuiwen told reporters at a briefing. Testing of imported "
        "chilled foods for the novel coronavirus during the second half of 2020 "
        "slowed imports but arrivals still kept up a healthy pace. December imports "
        "jumped 24% from the 775,000 tonnes brought in the prior month to 964,000 "
        "tonnes, close to the monthly record hit in July 2020, as buyers stocked up "
        "for the peak consumption season during the upcoming Lunar New Year. But "
        "aggressive restocking of China’s pig farms last year will lead to pork "
        "production growth of about 10% in 2021, according to a Rabobank forecast, "
        "pushing imports of the meat down by as much as 30% year on year."
    )
    assert r["created_at"] == "2021-01-14T02:51:55Z"
    assert r["tags"] == ["article", "reuters.com"]
    assert r["title"] == "UPDATE 3-China 2020 meat imports close to 10 mln tonnes, up 60% on year"
