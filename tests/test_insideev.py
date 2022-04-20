"""Test suit for PurdueSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.insideev import InsideEvSpider
import pytest


@pytest.fixture()
def spider():
    return InsideEvSpider()


headers = headers(InsideEvSpider.name)
headers["User-Agent"] = InsideEvSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            InsideEvSpider.url,
            headers,
            [
                "https://insideevs.com/news/343447/fisker-reveals-long-range-electric-crossover-claims-sub-40000-price/",
                "https://insideevs.com/news/334834/refreshed-karma-revero-spied/",
                "https://insideevs.com/news/334443/henrik-fisker-discusses-emotion-automakers-future-in-rare-interview-we-tie-this-into-fiskers-past/",
                "https://insideevs.com/news/333698/karma-delivers-first-revero/",
                "https://insideevs.com/news/332339/loaded-karma-revero-checks-in-at-139900/",
                "https://insideevs.com/news/334094/fisker-emotion-to-be-fully-unveiled-august-17-new-images/",
                "https://insideevs.com/news/331651/karma-automotive-says-next-plug-in-vehicle-wont-be-atlantic/",
                "https://insideevs.com/news/330945/wanxiang-gets-final-approval-to-build-karma-revero-atlantic-plug-in-hybrid-in-china/",
                "https://insideevs.com/news/329536/karma-automotive-officially-opens-tech-center-in-troy-michigan/",
                "https://insideevs.com/news/331188/op-ed-karma-revero-an-old-school-zombie/",
                "https://insideevs.com/news/330873/karma-revero-to-be-sold-in-europe-starting-in-2018/",
                "https://insideevs.com/news/330868/to-ready-itself-for-revero-production-karma-will-move-to-new-irvine-california-hq/",
                "https://insideevs.com/news/330662/henrik-fisker-seeks-to-bring-back-classic-car-emotions-via-evs-video/",
                "https://insideevs.com/news/330506/karma-revero-50-miles-range-priced-north-of-115000-tesla-targeted/",
                "https://insideevs.com/news/330463/2017-karma-revero-unveiled-the-fisker-karma-lives-again-video/",
                "https://insideevs.com/news/330385/karma-announces-dealer-lineup-for-revero-sales-begin-this-year/",
                "https://insideevs.com/news/330367/wanxiang-to-build-375-million-ev-plant-in-china-will-produce-both-atlantic-and-karma/",
                "https://insideevs.com/news/331914/karma-expands-in-michigan-but-when-will-volume-revero-production-happen/",
                "https://insideevs.com/news/331516/karma-automotive-to-open-engineering-and-sales-office-in-troy-michigan/",
                "https://insideevs.com/news/330296/fisker-karma-to-spring-back-to-life-as-karma-revero-with-bmw-technology/",
                "https://insideevs.com/news/329411/new-info-on-2017-fisker-karma/",
                "https://insideevs.com/news/328492/breaking-karma-automotive-teams-with-bmw-on-electric-drive-charging-technology/",
                "https://insideevs.com/news/327162/fisker-automotive-changes-name-to-karma-automotive-launches-new-site/",
                "https://insideevs.com/news/327590/fisker-karma-production-to-finally-resume-in-2016/",
                "https://insideevs.com/fisker/karma/news/?p=2",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 25
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://insideevs.com/fisker/karma/news/?p=3",
            headers,
            [
                "https://insideevs.com/news/317097/fisker-karma-production-shutdown-now-exceeds-6-months/",
                "https://insideevs.com/news/317051/update-338-drowned-fisker-karmas-in-port-waiting-for-recall-fix/",
                "https://insideevs.com/news/317001/fisker-to-negotiate-new-contract-with-a123s-wanxiang-on-batteries-for-karma-hasnt-built-a-car-since/",
                "https://insideevs.com/news/316944/consumer-reports-reviews-the-model-s-guess-how-they-feel-about-it-video/",
                "https://insideevs.com/news/316917/bankrupt-a123-looks-to-break-fisker-battery-contract-threatens-karma-production/",
                "https://insideevs.com/news/316779/25-of-all-fiskers-in-us-sold-at-3-southern-californian-dealerships-many-of-those-at-event-last-week/",
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
            "https://insideevs.com/news/316779/25-of-all-fiskers-in-us-sold-at-3-southern-californian-dealerships-many-of-those-at-event-last-week/",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Fisker's US Dealerships - Get Selling Fisker Of Northwest "
        "Arkansas\nFisker has, at last count, 44 registered dealers in the "
        "United States, who have sold around 1,000 cars. However, about a quarter "
        "of those have been sold inside a 90 mile radius in California.\nOne Of "
        "28 Cars At Karma Event At Fisker HQ Last Month (photo via Fisker)\n28 "
        "of those thousand cars came home last week, as they took a ride down the "
        "Pacific Coast Highway after spending the morning at Fisker's global "
        "headquarters in Anaheim for the largest gathering of Karmas in "
        "history.\nEven Henrik Fisker himself was on hand for the event, "
        "and the company made sure to take advantage of the opportunity to promote "
        'that "range anxiety was non-existent, even as each made their way home '
        'after a catered lunch."\n“This is the first formal Fisker owner event '
        "and we hope to have many more,” said Henrik Fisker, Executive Chairman and "
        "Co-founder of Fisker Automotive. “Our team has worked hard to make Fisker "
        "the first to bring a car like the Karma to market. It was exciting to meet "
        "so many who share our vision of environmentally conscious cars that don’t "
        "sacrifice power, style or performance.”\nThe majority of the cars at "
        "the event came from Irvine's Fisker of Orange County, who also happens to "
        "lead the universe in Karmas sold at about 100 since the car went on sale "
        "last December. Just 50 miles north is Fisker of Santa Monica who is in "
        "second at just under 100 cars, and neighbor to the south in San Diego has "
        "notched 25 sales.\n“Southern Californians recognize the value of a car "
        "that perfectly fits their lifestyles,” said Marcelo Sandoval, "
        "sales manager at Fisker of Orange County. “Everything about the Karma, "
        "from the solar panel roof to the Fisker logo of a sunset over the Pacific "
        "Ocean, represents the lifestyle we love so much.” Sandoval was "
        "instrumental in organizing the event and bringing so many owners "
        "together.\nThe event also featured a tour of the Fisker design "
        "studios, that included a talk with the staff, and a close up look at the "
        "upcoming (sometime in 2014) Fisker Atlantic.\nFisker Press Release\n"
        "Orange County Register"
    )
    assert r["created_at"] == "2012-09-05T00:00:00+00:00"
    assert r["tags"] == ["FSR", "article", "insideevs-FSR"]
    assert (
        r["title"]
        == "25% Of All Fiskers In US Sold at 3 Southern Californian Dealerships, Many Of Those At Event Last Week"
    )


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://insideevs.com/news/343447/fisker-reveals-long-range-electric-crossover-claims-sub-40000-price/",
            headers,
        ),
    ],
)
def test_created_at(spider, response):
    r = next(spider.parse_article(response))
    assert r["created_at"] == "2019-03-18T00:00:00+00:00"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://insideevs.com/news/317119/fisker-on-the-hunt-for-partner-investor-in-china-hires-consulting-group-to-conserve-cash/",
            headers,
        ),
    ],
)
def test_text_ony(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == """It's no secret that Fisker Automotive is seeking a partner of some sorts to assist the struggling automaker, but it is news that Fisker has execs on the ground in China who are seeking serious investors to "save" the startup automaker. According to the Wall Street Journal , Fisker's CEO, Tony Posawatz, along with other top-level members of the Fisker Automotive team, have been the China, perhaps on several occasions, in search of investors interested in acquiring Fisker or at least some part of the automaker's range-extending technology. Is Fisker turning its back on the US? Fisker reportedly values its range-extending technology at $1 billion and it seems that several investors are interested in dealing. As the WSJ reports, at least two firms have hired banks to work on deals that may entice Fisker to sell. The Wall Street Journal says that Fisker is looking to finalize a deal by the end of next month. As we see it, Fisker needs to secure a massive investment if it is to stay in business for much longer. No Fisker Karmas built in six months . Development of the cheaper Fisker Atlantic has been put on hold indefinitely. This all seems to point to Fisker teetering on the edge of a potential shutdown, so it seems investments (perhaps even a buyout) are definitely needed at this point. In related news, Fisker Automotive hired Huron Consulting Group to assist the automaker in conserving cash as it seeks a investment bids expected to come in early February. Several global corporations are reportedly on the list of potential investors, as are automakers in China."""
    )
