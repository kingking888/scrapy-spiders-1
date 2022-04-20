"""Test suit for FarmDocDaily spider."""
from agblox.spiders.farmdocdaily import FarmDocDailySpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return FarmDocDailySpider()


headers_dict = headers(FarmDocDailySpider.host_header)
headers_dict["User-Agent"] = FarmDocDailySpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://farmdocdaily.illinois.edu/2020/12/coverage-levels-on-rp-relationship-to-premium-levels.html",
            headers_dict,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["url"]
        == "https://farmdocdaily.illinois.edu/2020/12/coverage-levels-on-rp-relationship-to-premium-levels.html"
    )
    assert r["text"] == (
        "In 2020, Revenue Protection (RP) was used on 93% of insured acres in Illinois, making it "
        "by far the most popular crop insurance product ( farmdoc daily , November 17, "
        "2020 ). Herein, we examine coverage levels while insuring with RP. Average coverage "
        "levels were high. Most farmers choose coverage levels such that premiums are between $15 "
        "and $23 per acre.\nCoverage Levels in Illinois\nThe highest RP coverage level is "
        "85%, with lower coverage levels available in 5% increments down to 50%. In 2020, "
        "44% of RP corn acres in Illinois were insured at an 85% coverage level, 35% at an 80% "
        "coverage level, and 16% at a 75% coverage level (see Figure 1). These three higher "
        "coverage levels accounted for 95% of the acres insured by RP.\nAverage coverage "
        "levels were calculated to summarize information. For example, the coverage-level "
        "information in Figure 1 was used to arrive at an average coverage level for corn in "
        "Illinois. In 2020, the average coverage level was 81%, with weights provided by acres "
        "insured. As can be seen in Figure 1, the 81% is composed of 44% of acres insured using "
        "an 85% coverage level, 35% at an 80% coverage level, and so on. Average coverage levels "
        "over 80% imply that the majority of acres were insured with 80% and 85% coverage levels."
        "\nAverage coverage levels in Illinois have increased since the introduction of revenue "
        "products in 1997, reaching their current level in 2013. The average coverage level since "
        "2013 has been stable at 81%.\nWhile stable over time, the average coverage level "
        "varies across the state (see Figure 2). In 2020, most counties in northern and central "
        "Illinois had average coverage levels above 80%. Most counties in southern Illinois had "
        "average coverage levels below 80%.\nRelationships Between Average Coverage Levels "
        "and Premiums\nCounties with higher coverage levels tend to have lower premiums than "
        "counties with lower coverage levels. To illustrate, Figure 2 shows farmer-paid premium "
        "for RP policies with 80% coverage levels. As can be seen in Figure 3, lower premiums "
        "occur in northern and central Illinois where average 80% premiums are usually between $7 "
        "and $14 per acre. Northern and central Illinois tend to have high coverage levels. On "
        "the other hand, many counties in southern Illinois had average premiums for 80% RP over "
        "$20 per acre. Southern Illinois tended to have lower average coverage levels.\nThe "
        "regional patterns suggest that farmers may make their coverage level choice to even out, "
        "or budget, their farmer-paid premium. Figure 4 shows average farmer-paid premium over "
        "all coverage level choices. The average premium in Figure 4 tend to even out over "
        "Illinois much more than the 80% premium shown in Figure 3.\nTo illustrate the "
        "budgeting process, take two counties that have their premiums colored orange in Figure "
        "4. DeKalb County is in northern Illinois and had an average premium across all coverage "
        "levels of $12 per acre. The 80% average premium was $7 per acre. In DeKalb County, "
        "a higher proportion of farmers took 85% coverage levels, thereby raising the average "
        "premium above the 80% premium. The average coverage level in DeKalb County was 84%, "
        "meaning that the vast majority of farms take RP at a 85% coverage level (see Figure 1). "
        "On the other hand, Jefferson County in southern Illinois had an average premium across "
        "all coverage levels of $17 per acre. An 80% coverage level had an average premium of $21 "
        "per acre. More farmers in Jefferson bought lower coverage levels y resulting in an "
        "average coverage level of 75% (see Figure 1).\nAcademic literature has evaluated "
        "this phenomenon (Bulut). Most farmers will only spend a certain amount on crop "
        "insurance. Values in the above figures suggest that many farmers will not spend over $15 "
        "to $23 per acre on crop insurance. Of course, variation in spending exists across "
        "farmers.\nAverage Coverage Levels Across the Midwest\nAverage coverage levels across "
        "the Midwest States are shown in Figure 4 for corn. Higher average coverage levels are "
        "located in the heart of the corn belt, with lower coverage levels radiating out from the "
        "middle of the Corn Belt. The correlation coefficient between average coverage levels and "
        "average premiums is -0.61. While that correlation is high, other factors influence "
        "coverage levels choice across the Midwest.\nCommentary\nMany farmers have settled on "
        "using RP at high coverage levels as their crop insurance coverage. Many farmers appear "
        "to make coverage level choices so as to keep premium levels below $15 to $23 per acre. "
        "Product type and coverage levels have been stable over several years. Crop insurance "
        "choices in 2021 likely will be much the same as those made in 2020.\nThis year, "
        "a new endorsement is available called the Enhance Coverage Option (ECO). ECO will "
        "provide county revenue coverage above the underlying RP policy in a band from 90 or 95% "
        "down to 86% (see farmdoc daily, November 24, 2020 ). One challenge this policy will face "
        "is premium costs. Aggregate statistics suggest that farmers place constraints on the "
        "amount they spend on crop insurance. Those constraints may prevent many farmers from "
        "buying the additional coverage. Purchases of ECO may be more likely in northern and "
        "central Illinois where premiums are lower."
    )
    assert r["created_at"] == "2020-12-01T00:00:00+00:00"
    assert r["tags"] == ["article", "farmdocdaily.illinois.edu"]
    assert r["title"] == "Coverage Levels on RP: Relationship to Premium Levels"
