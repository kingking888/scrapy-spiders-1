"""Test suit for Drovers."""

from agblox.spiders.drovers import DroversSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return DroversSpider()


headers = headers(DroversSpider.host_header)
headers["User-Agent"] = DroversSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            DroversSpider.url,
            headers,
            [
                "https://www.drovers.com/news/industry/hummus-cows",
                "https://www.drovers.com/news/industry/pork-drovers-recognized-editorial-excellence",
                "https://www.drovers.com/news/dairy-production/new-farmlink-project-helps-farmers-get-food-hungry-people",
                "https://www.drovers.com/news/industry/kansas-state-wins-national-livestock-judging-championship",
                "https://www.drovers.com/news/beef-production/selk-back-basics-revisiting-body-condition-scoring",
                "https://www.drovers.com/news/beef-production/tyson-foods-beats-profit-estimates-sees-lower-covid-19-costs-2021",
                "https://www.drovers.com/news/industry/american-angus-association-elects-new-officers-board-leadership",
                "https://www.drovers.com/news/industry/california-defeats-proposition-15",
                "https://www.drovers.com/news?page=1",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 9
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.drovers.com/news?page=1096",
            headers,
            [
                "https://www.drovers.com/news/afbf-retail-food-prices-rise-slightly-second-quarter",
                "https://www.drovers.com/news/bse-case-confirmed-canada",
                "https://www.drovers.com/news/consider-multiple-pasture-system-reduce-input-costs",
                "https://www.drovers.com/news/cattle-feed-inventory-down",
                "https://www.drovers.com/news/senate-action-puts-complete-farm-bill-law",
                "https://www.drovers.com/news/cattlemen-support-waiver-rfs-mandate",
                "https://www.drovers.com/news/animal-health-nutrition",
                "https://www.drovers.com/news/wind-new-corn-struggling-ag-producers",
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
            "https://www.drovers.com/news/glenn-selk-maintain-bcs-between-calving-breeding",
            headers,
        ),
    ],
)
def test_created_at(spider, response):
    r = next(spider.parse_article(response))
    assert r["created_at"] == "2020-10-28T01:48:15+00:00"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.drovers.com/news/nebraska-family-simplifies-feeding-cattle-management-app",
            headers,
        ),
    ],
)
def test_text_ony(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Jordan Gall is a third-generation cattle feeder, working alongside his brother and "
        "parents on G&A Farms, their family operation near Clarkson, Nebraska. They own and "
        "custom-finish cattle, manage a cow-calf herd, custom feed hogs and grow corn and "
        "soybeans.\nJordan recalls spending hours with pen and paper, calculating and "
        "recalculating numbers to get a better handle on their cattle business performance.\n“I "
        "wrote everything down in a book and would go through every group at the end of the "
        "month,” says Jordan. “I’d go through every number, every group to calculate inventory, "
        "breakeven and other needs.”\nThe Gall family used another software program before "
        "switching to Performance Beef , but difficulties with the program triggered the need for "
        "a change. Jordan noticed they were continually overfeeding.\n“Our other program told "
        "us what we were supposed to feed, but it didn’t measure what was being delivered,"
        "” says Jordan. “This is how I got my dad on Performance Beef. I calculated how much he "
        "was overfeeding with the other program and showed him what we were losing every month. "
        "It was clear that using Performance Beef was going to save us money in the long run.”\n"
        "Performance Beef’s simplicity made it a smooth transition. Often steering clear of new "
        "technology and even delaying adoption of a smartphone, Jordan’s dad is a good indicator "
        "of the ease of use. He quickly picked up Performance Beef, using it daily to set all the "
        "rations and loads as well as follow up to check feeding stats. “If he can use it, "
        "anyone can use it,” adds Jordan jokingly.\nThis cattle management software removed "
        "the guesswork.\n“We’re no longer throwing away feed and other costs. With Performance "
        "Beef every dollar is captured and accurate,” says Jordan. “Previously we were "
        "guesstimating based on a rough estimate of head in a pen. Now we know exactly what is in "
        "a pen, how they’re getting fed and are able to accurately capture all associated "
        "costs.”\nThe increased knowledge and clearer picture of their operation’s performance "
        "make it a no-brainer for the Galls.\n“I can honestly say I recommend Performance "
        "Beef to everybody I know who feeds cattle,” says Jordan. “Just the ease of the entire "
        "program and analytics behind it. You get so many more insights than relying on "
        "complicated programs or pen and paper. And it’s all on a handheld device. It’s just "
        "easy.”\nSponsored by Performance Livestock Analytics"
    )


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.drovers.com/news/industry/court-upholds-california-proposition-12",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Proposition 12, California’s 2018 ballot initiative that bans the sale of meat and eggs "
        "derived from producers that don’t meet California standards, was upheld by a panel of "
        "judges in the Ninth Circuit Court of Appeals on Thursday.\nA federal district court had "
        "rejected a request by the North American Meat Institute (NAMI) for a preliminary "
        "injunction against Proposition 12, and the three-judge panel on the US Court of Appeals "
        "upheld that decision. NAMI opposes Proposition 12 because it established meat production "
        "standards that apply to producers outside of the state.\n“We are disappointed in the "
        "ruling and are reviewing our options,” NAMI said. “California should not be able to "
        "dictate farming practices across the nation.”\nCalifornia voters approved the "
        "Prevention of Cruelty to Farm Animals Act (Proposition 12) in 2018, which stipulates "
        "farmers must provide 43 square feet of floor space for calves, 24 square feet for pigs "
        "and more than one foot for hens. NAMI argued that Proposition 12 violates the commerce "
        "clause of the U.S. Constitution through what amounts to a trade barrier, and that "
        "California law should not affect meat producers outside of the state.\nU.S. District "
        "Judge Christina Snyder disagreed, saying the law doesn’t prevent out-of-state businesses "
        "from selling their products outside of California. The Ninth Circuit court agreed, "
        "ruling that Proposition 12 “does not have a discriminatory purpose given the lack of "
        "evidence that the state had a protectionist intent,” and in determining that NAMI was "
        "unlikely to succeed on the merits of its commerce clause claim.\nThe California "
        "campaign for Proposition 12 was led by the Humane Society of the United States (HSUS), "
        "and the ballot initiative passed with 63% of the vote.\nRelated stories:\nMeat "
        "Institute Seeks To End California's Proposition 12"
    )
    assert r["created_at"] == "2020-10-19T17:09:11+00:00"
    assert r["tags"] == ["slaughter cattle", "article", "drovers.com"]
    assert r["title"] == "Court Upholds California Proposition 12"
