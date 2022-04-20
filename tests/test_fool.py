"""Test suit for FoolSpider."""

from agblox.spiders.fool import FoolSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return FoolSpider()


@pytest.fixture()
def test_kwargs():
    return {"ticker": "fsr", "last_url": None}


headers = headers("www.fool.com")
headers["User-Agent"] = FoolSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.fool.com/investing/2020/11/02/nio-fisker-drive-markets-higher-norwegian-sinks-cr/",
            headers,
        ),
    ],
)
def test_article(spider, response, test_kwargs):
    r = next(spider.parse_article(response=response, **test_kwargs))
    assert (
        r["url"]
        == "https://www.fool.com/investing/2020/11/02/nio-fisker-drive-markets-higher-norwegian-sinks-cr/"
    )
    assert r["text"] == (
        "The first trading day of November brought a rally to Wall Street, as "
        "investors sought to claw back some of the losses from the previous week's "
        "market action. It's not as though any of the concerns that market "
        "participants have gone away over the weekend, as COVID-19 case counts "
        "remained high and Tuesday's presidential election promises to create plenty "
        "of drama. However, investors seemed willing to see at least the possibility "
        "that markets might not do a repeat of the bear market from late February and "
        "March. As of 10 a.m. EST, the was up 376 points to 26,878. The gained 47 "
        "points to 3,317, and the moved higher by 154 points to 11,065. In uncertain "
        "times, investors like to stick with what works, and that was evident from "
        "the appetite for shares of electric-vehicle manufacturers and . Meanwhile, "
        "cruise ship stocks continued to feel the pain, and even as a key regulatory "
        "block went away, shares of reacted to downbeat news. An electric performance "
        "Shares of electric automakers NIO and Fisker sprang out of the gate on "
        "Monday. The two stocks were neck and neck, both rising 12% at 10 a.m. EST.\n"
        "For NIO, good news on October sales justified the big up move. October "
        "delivery figures came in at 5,055, doubling last year's 2,526 delivery "
        "count. NIO's product mix was impressive, as the Chinese automaker sold 2,695 "
        "of its ES6 SUVs, 1,477 larger ES8 SUV models, and 883 of the company's "
        "latest EC6 coupe SUVs. Year to date, NIO is on pace to more than double its "
        "annual delivery count from 2019. Meanwhile, Fisker's gains came as investors "
        "finally seemed to realize that the company had . The company was the buyout "
        "target of special purpose acquisition company Spartan Energy Acquisition, "
        "and Fisker adopted its new ticker at the beginning of last Friday's trading "
        "session. Orders for the much-anticipated Ocean SUV have been strong, and "
        "Fisker has a whole line of products planned for future years. Electric car "
        "companies have been popular, and it'll be interesting to see how Fisker in "
        "particular does. Even with some having given up their early gains, Fisker "
        "and NIO have the potential to do well if they can keep up their momentum. "
        "Norwegian keeps passengers onshore a little longer Meanwhile, Norwegian "
        "Cruise Line Holdings suffered a 6% drop. The cruise operator has finally "
        "pulled the plug on operations for the rest of the year, even though a "
        "regulatory decision seemed to open the possibility of a return to normal "
        "operating conditions sooner than that. Norwegian said it would suspend all "
        "of its cruises scheduled between now and Dec. 31. The company had already "
        "given up on November cruises, but the elimination of December sailings came "
        "as a surprise to many. The move came despite the fact that the Centers for "
        "Disease Control and Prevention allowed its no-sail order to expire on Oct. "
        "31. In its place, the that set up a phased-in approach toward returning "
        "Americans to the high seas. Norwegian's decision was disappointing, but it "
        "makes sense that the cruise operator will need time to convince regulators "
        "that it has the health and safety protocols in place to handle COVID-19 "
        "outbreaks safely if they occur. Unfortunately, other cruise lines are likely "
        "to follow suit, ending hopes among travelers to get on board as soon as "
        "possible."
    )
    assert r["created_at"] == "2020-11-02T00:00:00+00:00"
    assert r["tags"] == ["equity", "fool", "article", "FSR"]
    assert r["title"] == "NIO, Fisker Drive Markets Higher; Norwegian Sinks Cruise Ship Stocks"
