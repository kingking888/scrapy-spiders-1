"""Test suit for BeefMagazine."""

from agblox.spiders.beefmagazine import BeefMagazineSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return BeefMagazineSpider()


headers = headers(BeefMagazineSpider.host_header)
headers["User-Agent"] = BeefMagazineSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            BeefMagazineSpider.url,
            headers,
            [
                "https://www.beefmagazine.com/beef/faith-and-food-how-beliefs-shape-food-choices-part-3-kosher-programs",
                "https://www.beefmagazine.com/beef/packer-gross-margins-following-covid-19",
                "https://www.beefmagazine.com/beef/anticipating-change-drive-beef-industry-success",
                "https://www.beefmagazine.com/beef/thank-you-and-farewell",
                "https://www.beefmagazine.com/beef/its-been-heckuva-ride",
                "https://www.beefmagazine.com/beef/pcrm-targets-beef-industry-during-pandemic",
                "https://www.beefmagazine.com/beef/problem-things-we-know-just-aint-so",
                "https://www.beefmagazine.com/beef/heres-why-china-going-boom",
                "https://www.beefmagazine.com/beef/price-trends-comparing-cattle-cash-and-formula-prices",
                "https://www.beefmagazine.com/beef/promote-herd-health-preventing-scours",
                "https://www.beefmagazine.com/livestock?page=1&infscr=1",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 11
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.beefmagazine.com/livestock?page=860&infscr=1",
            headers,
            [
                "https://www.beefmagazine.com/mag/beef_nichols_onesource_genetics",
                "https://www.beefmagazine.com/beef/4-nutritional-headlines-endorse-meat",
                "https://www.beefmagazine.com/marketing/2018-cow-slaughter-numbers-review",
                "https://www.beefmagazine.com/technology/blockchain-lights-out-approach-supply-chain-efficiency",
                "https://www.beefmagazine.com/animal-welfare/will-veterinary-feed-directive-make-cleaner-water",
                "https://www.beefmagazine.com/beef-quality/do-best-pregnancy-diets-center-around-meat",
                "https://www.beefmagazine.com/seedstock-100/seedstock-100-consolidation-set-continue",
                "https://www.beefmagazine.com/cowcalfweekly/0624-pushing-weaning-envelope",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 8
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.beefmagazine.com/animal-health/contaminated-surroundings-risk-fmd-spread",
            headers,
        ),
    ],
)
def test_created_at(spider, response):
    r = next(spider.parse_article(response))
    assert r["created_at"] == "2020-09-08T17:46:24+00:00"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.beefmagazine.com/animal-health/7-ag-stories-you-might-have-missed-week-oct-23-2020",
            headers,
        ),
    ],
)
def test_text_ony(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Missed some ag news this week? Here are seven stories to catch you up.\n1. Farm "
        "Credit leaders provided an overview of how COVID-19 has impacted agriculture at a "
        "national level, in the northeast and in the nation's midsection this week. Federal "
        "dollars were key, the leaders said. – Farm Futures\n2. A new study from the Centers "
        'for Disease Control suggests that "Hispanic or Latino, non-Hispanic Black, '
        "and non-Hispanic Asian/Pacific Islander workers . . . might be disproportionately "
        'affected by COVID-19" in agriculture and manufacturing workplaces. The CDC compared data '
        "for food manufacturing and agriculture workers in 30 states, with 742 companies "
        "reporting a total of 8,978 cases and 55 deaths. – Today\n3. Agricultural ministers "
        "from European Union member states have reached an agreement on reforming the Common "
        "Agricultural Policy . The deal will place a bigger focus on environmental protection. – "
        "DW\n4. AppHarvest opened its first high-tech greenhouse in Morehead, Kentucky, "
        "on Oct. 21. The 2.76-million-square-foot building is considered one of the world's "
        "largest high-tech greenhouses. It will employee more than 300 people and produce 45 "
        "million pounds of tomatoes annually. – Lexington Herald-Leader\n5. Hemp farmers cite "
        "the THC limit as one of the most challenging aspects of cultivation. Weather conditions "
        "or stressors can cause the THC level to spike and if the level spikes, the plant can't "
        "be used for fiber, food or a variety of industrial products. – The Columbus "
        "Dispatch\n6. Imports of frozen beef are up nearly 20% since the coronavirus pandemic "
        "began slowing processing at U.S. meat packing plants. Imports from Nicaragua have "
        "soared, with the country becoming the third largest supplier of frozen beef to the U.S. "
        "Violence is occurring in the country with armed cattle ranchers attacking Indigenous "
        "communities to take their land for cattle ranching. Most U.S. consumers have no way of "
        "knowing where their beef is coming from because U.S. importers aren't required to "
        "disclose where beef comes from. – PBS\n7. Germany has reported 80 cases of African "
        "swine fever since Sept. 10. All have been in wild pigs. - Metro\nAnd your "
        "bonus.\nLarson Farms takes viewers along on the last day of corn harvest 2020 . – "
        "YouTube"
    )


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.beefmagazine.com/beef/7-ag-stories-you-might-have-missed-week-aug-7-2020",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Missed some ag news this week? Here are 7 agricultural stories to catch you up.\n1 "
        ".A new farmer survey by Farm Futures found 2020 corn yield projections to increase 11.5 "
        "bushels per acre from 2019 to 178.9 bpa. Growers in Farm Futures’ survey estimated 2020 "
        "yields at 51.0 bpa, up 3.6 bpa from 2019. Farm Futures survey respondents expect to see "
        "a 1.8 bpa drop in wheat yields in 2020. – Farm Futures\n2. Farm bankruptcies "
        "increased 8% over a 12-month period, with 580 filings from June 2019 to June 2020. A "
        "six-month comparison, however, shows the number of new Chapter 12 filings slowing. The "
        "Midwest, Northwest and Southeast were hardest hit, representing 80% of the filings "
        "across the U.S. Wisconsin led the nation with 69 filings, followed by 38 in Nebraska and "
        "36 apiece in Georgia and Minnesota. – Wallace's Farmer\n3. Are you counting the days "
        "to the Election 2020? In columns this week, Gary Baise and Jacqui Fatka tackle the "
        "presidential campaign. Biden’s Rural Plan calls for promoting ethanol and "
        "next-generation biofuels and investing $400 billion in clean energy research, innovation "
        "and deployment. The Democratic party's draft 2020 platform has 10 sections, Baise said, "
        "but agriculture isn't among them. – Farm Futures\n4. As harvest season approaches, "
        "residents and migrant laborers in rural communities are at risk from COVID-19. Across "
        "the U.S., rural communities have been largely spared the worst of the pandemic, "
        "butt the influx of new people who live together in tight quarters raises fears of "
        "outbreaks. – The Hill\n5. Indigo Ag has raised more than $300 million to reward and "
        "train farmers to use regenerative farming practices. – CNBC\n6. The Health, "
        "Economic Assistance, Liability Protection and Schools Act contains $20 billion to "
        "continue USDA responses to the pandemic. It also includes $457 million to address other "
        "issues, including rural rental assistance. – Forbes\n7. Agri Beef plans to open a "
        "new beef processing plant in south central Idaho. The company owns Snake River Farms and "
        "Double R Ranch brands. The plant will be able to process 500 cattle a day. – Idaho "
        "Business Review\nAnd your bonus.\nThe J.C. Adams Stone Barn in Montana's Sun "
        "River Valley was completed in 1885, four years before Montana became a state. It's been "
        "registered as a National Historic Place since 1979. It was recently restored. - KXLH"
    )
    assert r["created_at"] == "2020-08-07T13:13:17+00:00"
    assert r["tags"] == ["slaughter cattle", "article", "beefmagazine.com"]
    assert r["title"] == "7 ag stories you might have missed this week - Aug. 7, 2020"
