"""Test suit for PennStateSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.penn_state import PennStateSpider
import pytest


@pytest.fixture()
def spider():
    return PennStateSpider()


headers = headers(PennStateSpider.name)
headers["User-Agent"] = PennStateSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            PennStateSpider.url,
            headers,
            [
                "https://extension.psu.edu/2020-results-pa-commercial-grain-and-silage-hybrid-corn-tests-report",
                "https://extension.psu.edu/multi-benefit-plants-in-the-landscape",
                "https://extension.psu.edu/so-you-need-to-find-recertification-credits-we-can-help",
                "https://extension.psu.edu/fescue-toxicity",
                "https://extension.psu.edu/what-should-you-do-with-spotted-lanternfly-egg-masses",
                "https://extension.psu.edu/hoyas-as-houseplants",
                "https://extension.psu.edu/easy-cooking-from-pantry-to-home-newsletters",
                "https://extension.psu.edu/canning-on-smooth-cooktops",
                "https://extension.psu.edu/time-temperature-pressure-in-canning-foods",
                "https://extension.psu.edu/when-a-jar-becomes-unsealed",
                "https://extension.psu.edu/water-tests-for-households-using-public-water-supplies",
                "https://extension.psu.edu/simple-hydroponics",
                "https://extension.psu.edu/tree-of-heaven",
                "https://extension.psu.edu/preserving-fall-apples",
                "https://extension.psu.edu/rain-rot-in-horses",
                "https://extension.psu.edu/horse-management-during-wet-weather",
                "https://extension.psu.edu/salmonellosis",
                "https://extension.psu.edu/the-argument-for-houseplants",
                "https://extension.psu.edu/dairy-outlook-october-2020",
                "https://extension.psu.edu/pepper-production",
                "https://extension.psu.edu/salpingitis-salpingoperitonitis",
                "https://extension.psu.edu/african-violet-care",
                "https://extension.psu.edu/onion-production",
                "https://extension.psu.edu/staphylococcosis-in-chickens",
                "https://extension.psu.edu/colibacillosis-in-chickens",
                "https://extension.psu.edu/administradores-vs-lideres-diferentes-pero-igualmente-importantes",
                "https://extension.psu.edu/managers-vs-leaders-different-but-equally-important",
                "https://extension.psu.edu/crop-disorders-of-chickens-ii-ingluvitis",
                "https://extension.psu.edu/crop-disorders-of-chickens-i-crop-impaction",
                "https://extension.psu.edu/fall-forage-management",
                "https://extension.psu.edu/guidance-for-indoor-farmers-markets-under-covid-19",
                "https://extension.psu.edu/removing-cows-from-the-dairy-herd-during-changing-market-conditions",
                "https://extension.psu.edu/managing-dry-cows-to-reduce-mastitis-in-the-future",
                "https://extension.psu.edu/cull-rates-how-is-your-farm-doing",
                "https://extension.psu.edu/impacts-of-lameness-part-2-strategies-for-identifying-lame-cows",
                "https://extension.psu.edu/achieving-a-healthy-weaning-transition",
                "https://extension.psu.edu/dairy-sense-planning-forage-inventory-for-2021",
                "https://extension.psu.edu/cannibalism-in-chickens",
                "https://extension.psu.edu/what-should-i-do-with-all-my-home-canned-food",
                "https://extension.psu.edu/2020-beef-sired-progeny-from-dairy-cows",
                "https://extension.psu.edu/reproduccion-en-vacas-lecheras-101-anatomia-y-funcion-de-la-vaca-lechera",
                "https://extension.psu.edu/bacterias-coliformes",
                "https://extension.psu.edu/plomo-en-el-agua-potable",
                "https://extension.psu.edu/nitratos-en-el-agua-potable",
                "https://extension.psu.edu/mareks-disease-in-chickens-description-and-prevention",
                "https://extension.psu.edu/is-your-n95-respirator-fact-or-fiction",
                "https://extension.psu.edu/safe-uses-of-agricultural-water",
                "https://extension.psu.edu/feed-inventory-for-the-dairy-herd-planning-for-shortages",
                "https://extension.psu.edu/meaningful-engagement-for-people-with-dementia",
                "https://extension.psu.edu/how-forest-carbon-programs-work-two-case-studies",
                "https://extension.psu.edu/shopby/articles?limit=50&mode=list&p=2",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 51
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://extension.psu.edu/shopby/articles?limit=50&p=108",
            headers,
            [
                "https://extension.psu.edu/white-clover",
                "https://extension.psu.edu/some-facts-about-soil-basics",
                "https://extension.psu.edu/birdsfoot-trefoil",
                "https://extension.psu.edu/forage-quality-in-perspective",
                "https://extension.psu.edu/control-of-summer-annual-grass-weeds-in-turfgrasses",
                "https://extension.psu.edu/red-clover",
                "https://extension.psu.edu/reed-canarygrass",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 7
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://extension.psu.edu/what-should-you-do-with-spotted-lanternfly-egg-masses",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == """Spotted lanternfly (SLF) egg masses are laid in the late summer and into the early winter, with the majority of egg mass deposition occurring in October. These egg masses survive winter and hatch into SLF nymphs in the spring. Each egg mass contains an average of 30-50 eggs, and an individual female can lay at least 2 egg masses. These egg masses are the only stationary stage of the SLF, making them an easy target for removal. However, there are a few things you should know before you proceed to squash and scrape! Identifying Egg Masses SLF egg masses are usually about 1.5 inches long and colored brown/grey; however there can be a lot of variation among them! All egg masses contain rows of small eggs, roughly the size of a sharpened pencil point. Rows can vary in length, with some being longer than others in the same egg mass. Eggs within the egg mass can vary in color from a yellow to brown. After the female lays the eggs, she covers them with a substance believed to help them survive winter conditions and protect them from predation. When this substance is first deposited, it is white and glossy. After a few hours, the substance becomes duller and dries to a darker grey/brown color. Some egg masses do not get covered, often because the female SLF was disturbed by outside factors such as humans, other SLF, or potential predators. We have found that egg masses without a covering have a 10% lower hatch rate on average, though they can still hatch. Egg masses that have not been laid by the female will not hatch – if you kill an adult female SLF that is full of eggs, you need not do more! Variations in spotted lanternfly egg masses including color (yellow, gray, brown) and covering. Photo Heather Leach. Egg mass cases that were laid up to 2 years ago can still be found on trees and other structures – the easiest way to distinguish a fresh egg mass from an old one is to (1) check for the presence of the covering on the top of the egg mass and (2) check for the presence of emergence holes. The covering fades with time and while it is often still present in the spring, it may look dry and cracked. After the eggs hatch in the spring, the remnants of the egg mass weather even more, making the covering often disappear altogether. Additionally, each egg mass is equipped with a top “hatch door” that nymphs use to escape out of in the spring. These emergence holes are a perfect oval at the top of each egg. If these are present, the egg mass is old and nymphs have already hatched from it. A wooden post abundant with spotted lanternfly egg masses. Spotted lanternfly females prefer to lay eggs next to already existing egg masses. Photo Heather Leach. Locating the Egg Masses Female SLF will lay their eggs in a variety of places, most commonly on trees next to their feeding site. Often, the hosts preferred by SLF in the late season is red maple, silver maple, and willows - this is an excellent place to start looking for egg masses! However, SLF will also lay eggs on trees they do not heavily feed on, including black cherry and pine trees. It is important to keep in mind that you will not be able to reach all of the egg masses deposited on a tree; in fact, on average less than 2% of the egg masses laid on a tree are at a reachable distance (0-10ft) on the tree, leaving 98% of the egg masses above reach. Note that these numbers were taken from maples between 30-40 feet high and may differ for other tree species or different sized trees. We do not recommend using ladders or climbing trees to get to the unreachable distance. Keep in mind that each egg mass killed can remove up to 50 SLF from next year’s generation, but you are unlikely to get them all. Continued management strategies on nymphs and adults next year, such as tree traps, may be necessary. Read more about other management strategies for SLF here: " Spotted Lanternfly Management for Residents ." SLF prefer to lay egg masses in protected areas such as the undersides of tree limbs, picnic tables, and other outdoor surfaces that are horizontal or angled toward the ground. Currently, we are trying to determine which substrates they prefer to lay on the most. Interestingly, we have found that SLF females prefer to lay eggs near other SLF egg masses, so you will often see SLF egg masses clumped together. We are currently carrying out trials to determine what makes these egg masses attractive. Reporting Egg Masses SLF egg masses found in areas within most areas of the current quarantine zone do not need to be reported. However, if you find an egg mass within quarantined counties newly added in 2020 (Beaver, Allegheny, Blair, Huntingdon, Mifflin, Juniata, Perry, Cumberland, York, Northumberland, Columbia, and Luzerne), it is helpful to management and monitoring efforts if you destroy and report these. If you find a SLF egg masses outside of the quarantine zone, it should be reported immediately and destroyed. Follow the guidelines below for how to properly destroy it. If possible, take a picture of the egg mass before destroying it so that officials can confirm the sighting. You can report your find the Penn State Extension Spotted Lanternfly website or by calling our hotline 1-888-422-3359. Any egg mass found on plants or outdoor equipment that will be transported (e.g. camping equipment, vehicles) should be removed and inspected thoroughly before moving them. The SLF checklist for residents, found at the Spotted Lanternfly website , can help guide you through this inspection process. If you are a business transporting any vehicles or conveyances with the SLF quarantine zone, a SLF permit issued by the PA Department of Agriculture is required. To obtain the required training and permit, you can visit the Penn State Extension Spotted Lanternfly website . Scraping or Smashing Egg Masses Scraping spotted lanternfly egg masses into a plastic bag from a cinder block. Photo Nancy Bosold. If you find egg masses on your property from September to May, you can scrape them off using a plastic card or putty knife. Scrape them into a bag or container filled with rubbing alcohol or hand sanitizer and keep them in this solution permanently. Egg masses that are scraped to the ground can still hatch, so it is important to follow all steps! Egg masses can also be smashed, but be sure to apply even and forceful pressure to the entire egg mass. A properly smashed egg will burst open. You can learn more about this method by watching our how-to video: " How To Remove Spotted Lanternfly Eggs ." Remember that some eggs will be very difficult or even unreachable at the tops of trees, in other well-hidden areas, and they may be present throughout your neighborhood and community. Be aware that this method may reduce the number of nymph or adult SLF you see later in the year but most likely will not eliminate the population completely from your area. Using Ovicides on Egg Masses Based on studies done in 2018 and 2019, our results suggest some insecticides have ovicidal action against SLF eggs. All studies were done on intact egg masses (with covering) between February and April. Although many synthetic insecticides were tested against SLF eggs, the most effective products tested were paraffinic and/or mineral oils such as JMS Stylet oil, Damoil and Lesco Horticultural oil, commonly used in fruit systems as insecticides to control soft bodied insects. Many of these oils are also available to residents at local garden centers. When oils were applied at a solution of at least 3 percent, they were effective in killing up to 75 percent of treated eggs. One of the most important parts to getting effective control is to make sure you have good coverage and apply the oil solution directly to the egg masses. The only plant-based oil, soybean oil, had similar control of SLF egg masses when applied at a 50% concentration. Oils, when applied at the correct time and with good coverage, can offer some control of egg masses and have very little non-target effects. The use of oils provides not only a safe, environmentally friendly option but also provides control to some egg masses that are not accessible for physical removal or smashing. However, for egg masses that are within a reachable area, smashing or scraping the egg masses will provide greater efficacy than the ovicides currently available. We are actively researching other ovicides that could provide increased control and encourage you to stay up to date on our progress!"""
    )
    assert r["created_at"] == "2020-11-04T00:00:00+00:00"
    assert r["tags"] == ["article", "extension.psu.edu"]
    assert r["title"] == "What Should You Do With Spotted Lanternfly Egg Masses?"
