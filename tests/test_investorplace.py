"""Test suit for InvestorPlaceSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.investorplace import InvestorPlaceSpider
import pytest


@pytest.fixture()
def spider():
    return InvestorPlaceSpider()


headers = headers(InvestorPlaceSpider.name)
headers["User-Agent"] = InvestorPlaceSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            InvestorPlaceSpider.url,
            headers,
            [
                "https://investorplace.com/2020/11/try-a-small-position-in-fsr-stock-but-monitor-the-competition/",
                "https://investorplace.com/2020/10/history-doesnt-bode-well-for-spaq-stock-as-wall-street-goes-nuts-for-evs/",
                "https://investorplace.com/2020/10/stay-sidelines-spaq-stock-single-digits/",
                "https://investorplace.com/2020/10/4-top-stock-trades-for-monday-twlo-snap-spaq-gild/",
                "https://investorplace.com/2020/10/why-spaq-stock-is-an-electric-buy-before-its-ev-merger/",
                "https://investorplace.com/2020/10/spaq-stock-is-only-for-those-who-can-handle-the-heat/",
                "https://investorplace.com/2020/10/spac-ipos-are-hot-but-not-all-of-them-will-deliver-for-investors/",
                "https://investorplace.com/2020/10/spaq-stock-should-rise-soon-but-then-volatility-ensues/",
                "https://investorplace.com/2020/10/spaq-stock-right-stock-wrong-time/",
                "https://investorplace.com/2020/10/risk-haters-consider-magna-than-spaq-stock-spartan-energy-acquisition/",
                "https://investorplace.com/2020/10/spa-stock-road-to-nowhere/",
                "https://investorplace.com/2020/10/4-top-stock-trades-for-monday-pton-pfe-fsly-spaq/",
                "https://investorplace.com/2020/10/spaq-stock-merger-target-fisker-signs-to-make-ev-ocean-suv-in-europe/",
                "https://investorplace.com/2020/10/spaq-stock-merger-fisker-closes-soon-pushing-up-the-stock/",
                "https://investorplace.com/2020/10/investors-should-employ-the-wait-and-see-approach-with-spaq-stock/",
                "https://investorplace.com/2020/10/spaq-stock-is-likely-to-be-volatile-in-october/",
                "https://investorplace.com/2020/10/what-is-spartan-energy-acquisition-spaq-stock-and-is-it-a-buy-cseo/",
                "https://investorplace.com/2020/10/will-spaq-stock-crash-like-nikola-stock-did/",
                "https://investorplace.com/2020/10/it-looks-like-spartan-energy-stock-will-ride-this-electric-vehicle-stocks-rally/",
                "https://investorplace.com/2020/10/spaq-stock-has-ev-ambitions-relying-solely-on-fisker/",
                "https://investorplace.com/stock-quotes/spaq-stock-quote/page/2/",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 21
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://investorplace.com/stock-quotes/spaq-stock-quote/page/4/",
            headers,
            [],
        ),
    ],
)
# this last page doesnt have any articles from investor place, only articles from other pages
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == 0
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://investorplace.com/2020/07/ev-news-boosts-spaq-stock-higher/",
            headers,
        ),
    ],
)
def test_created_at(spider, response):
    r = next(spider.parse_article(response))
    assert r["created_at"] == "2020-07-10T00:00:00+00:00"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://investorplace.com/2020/07/ev-news-boosts-spaq-stock-higher/",
            headers,
        ),
    ],
)
def test_text_ony(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Spartan Energy (NYSE: SPAQ ) stock is on the rise Friday following news "
        "that the company is planning to acquire electric vehicle (EV) company "
        "Fisker .\nSource: buffaloboy / Shutterstock.com\nRecent reports "
        "claim that Spartan Energy is bidding to acquire the EV company . However, "
        "finer details of a possible deal, such as the asking price for Fisker or "
        "when the deal would close, are still completely unknown.\nIt’s worth "
        "pointing out that Spartan Energy isn’t a typical public company. Instead, "
        "its a special purpose acquisition company. It basically exists for the "
        "sole purpose of acquiring a private company and taking it public through a "
        "merger. This allows the company to avoid the typical initial public "
        "offering (IPO) process.\nAccording to the recent EV news, Spartan Energy "
        "isn’t the only company interested in acquiring Fisker. Unfortunately, "
        "it’s still unknown which other companies may be trying to purchase the "
        "carmaker, reports Bloomberg .\nIf Spartan Energy goes through with the "
        "acquisition, it would set Fisker up as a rival for other publically-traded "
        "EV companies. That includes the current market darling Tesla (NASDAQ: TSLA "
        "), as well as newer rivals, such as Nikola (NASDAQ: NKLA ).\nNikola "
        "actually saw its own rally earlier this week following some positive words "
        "from a JP Morgan analyst. That saw it getting a new rating and price "
        "target with the analyst expecting positive movement in the coming weeks."
        "\nSPAQ stock was up 8.6% as of Friday afternoon. It also saw a 38.5% jump "
        "on Thursday when the acquisition reports first started spreading.\nAs of "
        "this writing, William White did not hold a position in any of the "
        "aforementioned securities."
    )


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://investorplace.com/2020/08/fisker-spaq-stock-car-company-first-tech-firm-second/",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "With electric vehicle (EV) giant Tesla (NASDAQ: TSLA ) dominating the market it practically pioneered, there initially seems little point for competitors to directly challenge it. Sure, there are companies like Acrimoto (NASDAQ: FUV ) or Electrameccanica Vehicles (NASDAQ: SOLO ), but they fill niche segments. However, something like Fisker Inc. — which plans to go public with a merger via special-purpose acquisition corporation Spartan Energy Acquisition (NYSE: SPAQ ) — is a different animal altogether. Hence, the skepticism toward SPAQ stock.\nSource: Eric Broder Van Dyke / Shutterstock.com\nFisker Inc. and Spartan Energy Acquisition entered an agreement back in July that resulted in Fisker’s IPO under the SPAQ ticker. That said, the release announcing the partnership also mentions that it “…is expected to be completed in the fourth quarter of 2020… .”\nOverall, though, I completely get it. No matter how you break it down, SPAQ stock is a risky investment.\nAs you know, Henrik Fisker — founder, chairman and CEO of Fisker Inc. — previously attempted to build a business around a luxury EV called the Fisker Karma . And while the car attracted buzz from the automotive press and enthusiasts alike, the company failed. So, naturally, this will cause some hesitation toward those thinking about SPAQ stock.\nIn addition, Tesla utterly dominates the EV space thanks to its loyal and rapidly growing fanbase. Arguably, most of that success comes from Tesla’s vertical integration. And by controlling its battery pack production through its Gigafactory, Tesla has become the only high-volume EV manufacturer. Furthermore, the company can respond to various stimuli quickly .\nEssentially, all other direct EV competitors are well behind the eight-ball — and I appreciate this argument. When Apple (NASDAQ: AAPL ) launched its iPhone, it established the smartphone market and took over the entire portable phone space. It took years for competitors to put a dent in market share. And even today, you just don’t get the hype of a new iPhone release as you would from other smartphone brands.\nStill, that’s a different industry. We’re talking about cars, and that fact may help positively distinguish SPAQ stock.\nFirst and Foremost, SPAQ Stock Is an Automotive Investment\nWhile I’ve questioned the business decisions and sometimes erratic behaviors of Tesla CEO Elon Musk, I’ve never impugned his intelligence. Musk has been a national treasure — even though he was born in South Africa — promoting incredible innovations of applied science.\nBecause of this, however, Tesla is more of a technology company that makes cars. That said, what potentially makes SPAQ stock stand out is that Fisker is a car company that utilizes EV technology. And over time, consumers will recognize the difference.\nFor example, take the interior of the Tesla Model 3. In recent years, the Model 3 has incorporated a truly minimalist design . Upon entering the vehicle, what stands out to you the most is the lack of a dashboard. Rather than a car, the Model 3 interior — and to my understanding, other Teslas have adopted this design cue — resembles a work of art. Which is fine, except that it doesn’t resonate with car people.\nAlso, while minimalism is the new design theme for consumer tech products, I’m not sure it works in a car. As a driver, you want critical information to be displayed in a natural, intuitive location. Fisker understands this because the man is a legend in car design, with his handiwork previously gracing Aston Martin and BMW (OTCMKTS: BMWYY ). Therefore, Fisker Inc.’s Ocean SUV features an elegant but familiar dashboard.\nMoreover, the tremendous success of Tesla could turn out to be its biggest undoing later. Let’s be real: Tesla has been copying and pasting its cars for the last several years. So, when you see one, it’s no big deal.\nHowever, if you see one of these sexy Oceans driving around, you will do a double-take. It’s my opinion, yes, but the Ocean looks nothing like a Tesla .\nGreat Business Sense\nWhat I also appreciate about Fisker is the company’s business sense. Americans love SUVs . Therefore, it’s very sensible that Fisker is launching an SUV rather than a sedan or a sports car. It’s the same reason why Ford (NYSE: F ) attached its Mustang logo on its all-electric Mach-E.\nFisker and Ford are car companies. They understand the pulse of the automotive market, and are responding appropriately. And with Fisker, I don’t think you can ignore its price point. With the Ocean selling for $37,500 (potentially $30,000 with a federal tax credit), this deeply undercuts Tesla’s offerings.\nPlus, Fisker plans to outsource much of its manufacturing . Interestingly, Henrik Fisker noted that:\n“You can’t have a vertically integrated company where you do everything yourself…A lot of the hardware in vehicles is going to end up being a commodity, and therefore we are willing to share those parts with somebody else.”\nOverall, investors who are risk averse shouldn’t jump into SPAQ stock. A lot can go wrong when challenging a king. However, Fisker is different enough across the design and business elements that I believe it’s worth a bet.\nA former senior business analyst for Sony Electronics, Josh Enomoto has helped broker major contracts with Fortune Global 500 companies. Over the past several years, he has delivered unique, critical insights for the investment markets, as well as various other industries including legal, construction management, and healthcare. As of this writing, he is long SPAQ and F."
    )
    assert r["created_at"] == "2020-08-19T00:00:00+00:00"
    assert r["tags"] == ["FSR", "article", "investorplace.com-FSR"]
    assert r["title"] == "Why Fisker Inc. Is a Car Company First, And A Tech Firm Second"
