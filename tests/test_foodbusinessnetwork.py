"""Test suit for FoodBusinessNetwork spider."""

from agblox.spiders.food_business_news import FoodBusinessNewsSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return FoodBusinessNewsSpider()


headers = headers(FoodBusinessNewsSpider.host_header)
headers["User-Agent"] = FoodBusinessNewsSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            FoodBusinessNewsSpider.url,
            headers,
            [
                "https://www.foodbusinessnews.net/articles/17300-slideshow-new-menu-items-from-tgi-fridays-corner-bakery-cafe-peets-coffee",
                "https://www.foodbusinessnews.net/articles/17299-aak-to-build-plant-based-foods-center",
                "https://www.foodbusinessnews.net/articles/17297-kate-farms-raises-51-million-in-funding",
                "https://www.foodbusinessnews.net/articles/17271-sugar-reduction-innovation-intensifies",
                "https://www.foodbusinessnews.net/articles/17296-food-and-beverage-groups-urge-priority-access-to-covid-19-vaccine",
                "https://www.foodbusinessnews.net/articles/17159-interest-in-functional-ingredients-trending",
                "https://www.foodbusinessnews.net/articles/17295-sabra-selections-offers-consumers-choice-of-hummus-toppings",
                "https://www.foodbusinessnews.net/articles/17294-nestle-names-new-head-of-strategic-business-units",
                "https://www.foodbusinessnews.net/articles/17293-ferrero-hires-diversity-and-inclusion-director",
                "https://www.foodbusinessnews.net/articles/17292-chipotle-launches-first-digital-only-restaurant",
                "https://www.foodbusinessnews.net/articles/topic/96?page=2",
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
            "https://www.foodbusinessnews.net/articles/topic/96?page=547",
            headers,
            [
                "https://www.foodbusinessnews.net/articles/3102-campbell-sets-succession-plan-for-c-f-o-post",
                "https://www.foodbusinessnews.net/articles/3170-mcdonald-s-usa-taps-new-c-m-o",
                "https://www.foodbusinessnews.net/articles/3135-friendly-to-leave-general-mills",
                "https://www.foodbusinessnews.net/articles/3130-f-m-i-recognizes-campbell-s-morrison",
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
            "https://www.foodbusinessnews.net/articles/17159-interest-in-functional-ingredients-trending",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["url"]
        == "https://www.foodbusinessnews.net/articles/17159-interest-in-functional-ingredients-trending"
    )

    assert (
        r["text"]
        == "KANSAS CITY — Amid the uncertainty of a global pandemic, people are seeking to control that which they can control. They want to stay well, to think clearly and to sleep peacefully. They may be more likely to seek foods and beverages featuring ingredients that will help them reach those goals. “Certainly this idea of taking control of our health is one that functional products are bringing to the market,” said Laurie Demeritt, chief executive officer of The Hartman Group, Bellevue, Wash., in a Sept. 2 webinar. The popularity of functional ingredients may continue to rise even after COVID-19 fades. Market Research, Portland, Ore., forecasts the global functional food industry to have a compound annual growth rate of 6.7% from 2021 to 2027 and reach $267.92 billion, which would be up from $177.77 billion in 2019. “Although there is no industry-wide definition for functional ingredients, at FutureCeuticals we believe ‘functional ingredients’ go beyond nutrient density and provide specific health and wellness benefits,” said Ryan Wories, director of marketing for FutureCeuticals, Inc., Momence, Ill. “Functional ingredients allow the consumer to build personalized regimens to achieve their version of overall wellness and target key clinically researched body and mind fulfillment, exactly what today’s consumer is looking for.” The Hartman Group in April conducted an online national survey involving 2,367 US adults between the ages of 18 to 74. The survey showed Generation Z (ages 18 to 22), millennials (23 to 41), Generation X (42 to 55) and baby boomers (56 to 74) approach functional goals differently. Individuals in Generation Z tend to seek specific attributes, including improved digestion, bone strength, energy and sleep. Generation Z and millennials over-index in the inherently functional beverage space, Ms. Demeritt said. “Inherently functional foods and beverages do better than what we call fortified functional foods and beverages: the idea that being inherent is something that sort of is contributed to natural, less processed and fresh,” Ms. Demeritt said. Ingredients based on fruits and vegetables offer ways to create inherently functional products. Both elderberry and acerola are rising in popularity. Remedy Organics, Englewood Cliffs, NJ, has launched Berry Immunity, a plant-based protein beverage high in vitamin C and vitamin D content. It contains elderberry, strawberry, echinacea, camu camu, lion’s mane and prebiotics. “When creating Berry Immunity, I carefully selected a powerhouse of anti-viral ingredients that work synergistically to support the immune system,” said company founder Cindy Kasindorf. “Beyond superfood berries, herbs and mushrooms, prebiotics were a key component for further immune support and gut health, as 70% of your immune system lives in your gut.” FutureCeuticals’ ingredient portfolio includes a variety of whole foods that support immunity: acerola, orange, carrot, sweet potato, turmeric, quercetin, açai, maqui berry, kale and spinach. “We also offer branded solutions like Phyto-C,” Mr. Wories said. “Phyto-C is a new launch from Van Drunen Farms and FutureCeuticals. It is a plant-based, antioxidant complex that delivers 11 superfoods, including natural vitamin C and polyphenols, to help support a healthy immune response.” Phyto-C contains an excellent source of vitamin C, he added. The amount of vitamin C in 100 grams of acerola is 20 times the recommended daily intake, according to iTi Tropicals, Lawrenceville, NJ. Also known as Barbados cherry, acerola is grown commercially and harvested primarily in Brazil. A distinctive tart flavor allows it to blend well with other juices, particularly mango and pineapple juices, according to iTi Tropicals. Smoothies, jellies, jams, gummies and fruit snacks are other potential applications. The Hartman Group survey found 14% of respondents said they were consuming elderberry and another 52% said they were interested in trying it. “It just sort of coincided with this general interest in immunity,” Ms. Demeritt said. Eldermune, a new ingredient, combines elderberry juice concentrate for immune support and Sunfiber, a soluble prebiotic dietary fiber. Innovative Natural Solutions (INS Farms), Purdy, Mo., developed Eldermune. NutriScience Innovations, Trumbull, Conn., exclusively will supply and market it. Potential applications include beverages and dietary supplements. When working with elderberry or any functional ingredients, food and beverage companies should have proof to support their claims. A dietary supplement case provides a warning. Vitamin Bounty/Matherson Organics LLC discontinued Instagram and Facebook social media posts for its Vitamin Bounty Elderberry Immune Support following an inquiry by the National Advertising Division of BBB National Programs, which involve companies, industry experts and trade associations working together within a self-regulatory environment. The posts conveyed implied messages about boosting immunity to protect against or treat COVID-19, the NAD reported on Oct. 13. The NAD challenged this claim: “(a)s restrictions are gradually lifting, it’s more important than ever to keep your immune system strong. Our Elderberry Immune Support keeps you protected with vitamin C, zinc, elderberries, garlic and echinacea; a powerful immune-boosting combo.” Immunity made the list of top 10 trends for 2021 issued by Innova Market Insights, Arnhem, The Netherlands. Ongoing anxiety stemming from COVID-19 will encourage consumers to prioritize their immune health, according to Innova, which found about 60% of global consumers increasingly are looking for food and beverage products that support their immune health, with one in three saying concerns about immune health increased in 2020 over 2019. The Hartman Group survey found 19% of respondents already are using functional foods for immunity reasons and 48% are interested. The percentages for functional beverages were 13% and 46%. “It’s not that immunity wasn’t important before the pandemic, but certainly what is happening in the current environment has really pushed that to the top of the list,” Ms. Demeritt said. Lallemand, Inc., Montreal, offers probiotic strains L. rhamnosus Rosell-11 and L. helveticus Rosell-52 that are documented for immunity benefits, said Joanna Wozniak, business development manager for Lallemand Food Probiotics. The company’s LalDefense yeast beta-glucan supports the immune system by boosting people’s natural defenses. “These ingredients are inherently functional as they are ingredients we already find in nature and in our digestive system (yeast and bacteria) with their benefits as part of their nature,” Ms. Wozniak said. Boligo GOS from Ingredion, Inc., Westchester, Ill., supports digestive health and immune health, said Diane M. Nieto, senior manager, business development, starch-based texturizers in the United States and Canada for Ingredion. Boligo GOS is used in a variety of applications, including infant formula, dairy applications, cereal and beverages. Other Ingredion ingredients promote digestion, another functional benefit. Nutraflora short-chain fructooligosaccharides support digestive health and bone health. “It is selectively utilized and fermented by beneficial bacteria in the large intestine, making it a highly effective prebiotic fiber,” Ms. Nieto said. Hi-Maize high-amylose resistant starch, a type of fiber, also supports digestive health. People are showing an interest in trying functional foods that support cognition, reduce stress and help them sleep, according to The Hartman Group survey. While 14% said they use functional foods that support brain cognition/mental acuity, another 44% said they were interested in using them. The percentages for functional beverages were 10% and 44%. Generation Z consumers are more likely to be thinking about brain health, Ms. Demeritt said. “Obviously, they are thinking about it differently than older consumers,” she said. “It’s not about memory loss. It’s about staying sharp, staying on top of things and really retaining focus throughout the day.” Forty-eight percent of respondents said they were eating functional foods to help with sleep and rest, while 12% said they were interested in trying them. The percentages were 8% and 45% for functional beverages. Eleven percent said they were eating functional foods to reduce stress and anxiety, while 44% said they were interested in trying them. Startup company myAir, Ltd., Tel Aviv, Israel, has developed nutrition bars with a personalized edge. Each formulation contains a research-backed botanical blend designed to deliver a specific stress-relief effect. An online questionnaire profiles a person’s cognitive response to stress. Each bar is composed of a blend of nuts and fruits, and infused with a unique, research-based proprietary formula of bioactive botanical extracts. “As an executive manager and a mother, stress had become a massive burden in my life,” said Rachel Yarcony, founder and co-chief executive officer of myAir. “Good nutrition is a key to managing stress naturally. This spurred me to seek a natural solution and develop a ‘food for mood’ solution that consumers can easily merge into their daily routine to help take control of their health and manage their personal stress levels.”"
    )

    assert r["created_at"] == "2020-11-12T00:00:00+00:00"
    assert r["title"] == "Interest in functional ingredients trending"
