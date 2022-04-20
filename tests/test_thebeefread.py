"""Test suit for TexasCornSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.thebeefread import TheBeefReadSpider
import pytest


@pytest.fixture()
def spider():
    return TheBeefReadSpider()


headers = headers(TheBeefReadSpider.host_header)
headers["User-Agent"] = TheBeefReadSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            TheBeefReadSpider.url,
            headers,
            [
                "https://www.thebeefread.com/2020/11/17/fundamentals-diverge-as-virus-heats-up/",
                "https://www.thebeefread.com/page/2/",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 2
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.thebeefread.com/page/1604/",
            headers,
            [
                "https://www.thebeefread.com/2014/04/30/welcome/",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 1
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.thebeefread.com/2020/11/05/improvement-2/",
            headers,
        ),
    ],
)
def test_created_at(spider, response):
    r = next(spider.parse_article(response))
    assert r["created_at"] == "2020-11-05T11:49:43-06:00"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.thebeefread.com/2020/11/05/improvement-2/",
            headers,
        ),
    ],
)
def test_text_ony(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == """By Cassie Fish, http://cassandrafish.com\nThe most significant development in this week’s cash cattle trade is that north, after being discount, has returned to par with the south. Packers have paid $107 as readily in Nebraska as in Texas and Kansas and have paid up to $106 in Iowa. Since the north has been viewed as holding the cash market down, this is good news if bullish.\nTrade volume has been underway in earnest since yesterday and continues today. Volume is not huge but will certainly beat last week’s poor volume of 58k head. Packers continue to ask for time in many cases because the packer is fully aware boxed beef prices will seasonally advance over the coming 3-4 weeks. So the more cheap cattle inventory the packer owns the better. Plus fed cattle supplies remain somewhat tight for another 4-5 weeks.\nBoxed beef values are advancing seasonally posting choice at $211.50 this morning, a new high for the move. The choice cutout is headed to at least $220 by the end of the month.\nUSDA released the actual slaughter for week ended October 24 and once again the actual beat the estimate, this time by 2k head, the F.I. slaughter at 645k head. Steer carcass weights posted an all-time high at 931 pounds, up 2 pounds from the prior week. Weights will be topping very soon, though cattle feeding weather is phenomenal.\nCME live cattle futures are green and have made new highs for the move today. Take a look at an Apr LC chart or any month beyond Apr LC and the charts show prices have advanced above the 40-day and 100-day moving average and are trading at prices not seen since the second week in October. Dec and Feb LC are higher too, but the key resistance remains overhead.\nCME feeder cattle futures are trading lower because the grain and soy complex is on fire. Corn has stormed to new highs for the week and are eyeing the October high. Buying inspired by ideas of inflation seems to be infiltrating many different commodity markets. There is an old saying, “cheap grain, cheap cattle – high priced grain, high priced cattle”. The 2021 trend for corn – if prices average above $4 per bushel – increases cost of gain obviously, and will likely reduce days on feed and out-weights.\nCopyright © 2020 the Beef Read. All rights reserved\nThe Beef is published by Consolidated Beef Producers\nUse of part or all of this blog for any reason without permission is strictly prohibited.\nDisclaimer: The Beef, CBP, Cassie Fish nor NFC Frontier Capital Markets shall not be liable for decisions or actions taken based on the data/information/opinions.\nThis material has been prepared by a sales or trading employee or agent of New Frontier Capital Markets and is, or is in the nature of, a solicitation. This material is not a research report prepared by New Frontier Capital Markets. By accepting this communication, you agree that you are an experienced user of the futures markets, capable of making independent trading decisions, and agree that you are not, and will not, rely solely on this communication in making trading decisions. DISTRIBUTION IN SOME JURISDICTIONS MAY BE PROHIBITED OR RESTRICTED BY LAW. PERSONS IN POSSESSION OF THIS COMMUNICATION INDIRECTLY SHOULD INFORM THEMSELVES ABOUT AND OBSERVE ANY SUCH PROHIBITION OR RESTRICTIONS. TO THE EXTENT THAT YOU HAVE RECEIVED THIS COMMUNICATION INDIRECTLY AND SOLICITATIONS ARE PROHIBITED IN YOUR JURISDICTION WITHOUT REGISTRATION, THE MARKET COMMENTARY IN THIS COMMUNICATION SHOULD NOT BE CONSIDERED A SOLICITATION. The risk of loss in trading futures and/or options is substantial and each investor and/or trader must consider whether this is a suitable investment. Past performance, whether actual or indicated by simulated historical tests of strategies, is not indicative of future results. Trading advice is based on information taken from trades and statistical services and other sources that New Frontier Capital Markets believes are reliable. We do not guarantee that such information is accurate or complete and it should not be relied upon as such. Trading advice reflects our good faith judgment at a specific time and is subject to change without notice. There is no guarantee that the advice we give will result in profitable trades.\nPlease follow and like us:"""
    )


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.thebeefread.com/2020/10/29/on-fire-2/",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "By Cassie Fish, http://cassandrafish.com\nCME cattle futures are putting "
        "big time pressure on the managed fund shorts as most active Dec LC pushes "
        "over 300 points higher on the day. Technically the market is headed higher "
        "for the foreseeable timeframe and will be supported by improving "
        "fundamentals in November, a strong seasonal month for cash cattle and "
        "boxed beef prices.\nThe outlook is for higher cash cattle prices, "
        "which have a strong possibility of taking out the last swing cash cattle "
        "high of $108.26 and a shot of filling the gap on the cash chart left way "
        "back in June at $112.39. This would be a modest rally and would "
        "underperform the last 9 years. Southern feedlots, especially Texas are "
        "tight on numbers and will stay that way. The north will continue to trade "
        "discount as supplies are more ample and packers have lots of cattle bought "
        "with time.\nToday, bids of $106 in Texas are being passed, which are "
        "steady with last week. Boxed beef prices finally put on some money today "
        "also, the choice up $1.50.\nToday’s slaughter will be down as two Texas "
        "plants were forced to cancel their first shift because of poor road "
        "conditions related to snow. Some of this slaughter loss will be made up on "
        "Saturday.\nThe USDA announced the actual slaughter for the week ended "
        "Oct 17 and the industry slaughtered 5k more cattle than estimated bringing "
        "the total to 659k and the fed kill was 522k head. The fed kill has "
        "exceeded 2019 six out of the last eight weeks.\nCarcass weights for "
        "steers increased 1 pound to 929 pounds for that same week, a record and "
        "not a surprise for this year. Weights typically top in November.\n"
        "Copyright © 2020 the Beef Read. All rights reserved\nThe Beef is "
        "published by Consolidated Beef Producers\nUse of part or all of this "
        "blog for any reason without permission is strictly prohibited.\n"
        "Disclaimer: The Beef, CBP, Cassie Fish nor NFC Frontier Capital Markets "
        "shall not be liable for decisions or actions taken based on the "
        "data/information/opinions.\nThis material has been prepared by a sales "
        "or trading employee or agent of New Frontier Capital Markets and is, "
        "or is in the nature of, a solicitation. This material is not a research "
        "report prepared by New Frontier Capital Markets. By accepting this "
        "communication, you agree that you are an experienced user of the futures "
        "markets, capable of making independent trading decisions, and agree that "
        "you are not, and will not, rely solely on this communication in making "
        "trading decisions. DISTRIBUTION IN SOME JURISDICTIONS MAY BE PROHIBITED OR "
        "RESTRICTED BY LAW. PERSONS IN POSSESSION OF THIS COMMUNICATION INDIRECTLY "
        "SHOULD INFORM THEMSELVES ABOUT AND OBSERVE ANY SUCH PROHIBITION OR "
        "RESTRICTIONS. TO THE EXTENT THAT YOU HAVE RECEIVED THIS COMMUNICATION "
        "INDIRECTLY AND SOLICITATIONS ARE PROHIBITED IN YOUR JURISDICTION WITHOUT "
        "REGISTRATION, THE MARKET COMMENTARY IN THIS COMMUNICATION SHOULD NOT BE "
        "CONSIDERED A SOLICITATION. The risk of loss in trading futures and/or "
        "options is substantial and each investor and/or trader must consider "
        "whether this is a suitable investment. Past performance, whether actual or "
        "indicated by simulated historical tests of strategies, is not indicative "
        "of future results. Trading advice is based on information taken from "
        "trades and statistical services and other sources that New Frontier "
        "Capital Markets believes are reliable. We do not guarantee that such "
        "information is accurate or complete and it should not be relied upon as "
        "such. Trading advice reflects our good faith judgment at a specific time "
        "and is subject to change without notice. There is no guarantee that the "
        "advice we give will result in profitable trades.\nPlease follow and like "
        "us:"
    )
    assert r["created_at"] == "2020-10-29T11:54:13-05:00"
    assert r["tags"] == ["slaughter cattle", "article", "thebeefread.com"]
    assert r["title"] == "On Fire"
