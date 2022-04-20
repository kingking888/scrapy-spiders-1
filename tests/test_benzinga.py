"""Test suit for Benzinga."""

from agblox.spiders.benzinga import BenzingaSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def test_kwargs():
    return {"ticker": "TWTR", "last_url": None}


@pytest.fixture()
def spiderTWTR():
    return BenzingaSpider(url="https://www.benzinga.com/stock-articles/twtr/all")


@pytest.fixture()
def spiderFSR():
    return BenzingaSpider(url="https://www.benzinga.com/stock-articles/fsr/all")


headers_dict = headers(BenzingaSpider.host_header)
headers_dict["User-Agent"] = BenzingaSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.benzinga.com/stock-articles/twtr/all",
            headers_dict,
            [
                "https://www.benzinga.com/markets/options/20/12/18897911/9-communication-services-stocks-showing-unusual-options-activity-in-todays-session",
                "https://www.benzinga.com/markets/options/20/12/18876532/analyzing-twitters-unusual-options-activity",
                "https://www.benzinga.com/trading-ideas/long-ideas/20/12/18866426/will-snap-or-pinterest-stock-grow-more-by-2022",
                "https://www.benzinga.com/analyst-ratings/analyst-color/20/12/18855158/alphabet-twitter-top-online-media-recovery-stocks-for-2021-bofa",
                "https://www.benzinga.com/news/20/12/18849152/discord-doubles-valuation-to-7b-in-latest-funding-round",
                "https://www.benzinga.com/news/20/12/18847827/twitter-is-creating-a-new-account-type-just-for-bots",
                "https://www.benzinga.com/news/20/12/18848344/facebook-gets-another-advertiser-back-after-stop-hate-for-profit-campaign-unilever",
                "https://www.benzinga.com/news/earnings/20/12/18836066/moderna-vaccine-goes-into-fda-panel-hearing-today-raising-hope-of-another-tool-vs-virus",
                "https://www.benzinga.com/markets/options/20/12/18820580/9-communication-services-stocks-showing-unusual-options-activity-in-todays-session",
                "https://www.benzinga.com/news/20/12/18819718/stocks-that-hit-52-week-highs-on-wednesday",
                "https://www.benzinga.com/markets/penny-stocks/20/12/18819040/benzingas-top-upgrades-downgrades-for-december-16-2020",
                "https://www.benzinga.com/analyst-ratings/analyst-color/20/12/18817884/jpmorgan-upgrades-twitter-names-stock-one-of-our-top-picks",
                "https://www.benzinga.com/analyst-ratings/price-target/20/12/18813721/10-biggest-price-target-changes-for-wednesday",
                "https://www.benzinga.com/news/20/12/18812963/twitters-debt-overview",
                "https://www.benzinga.com/news/20/12/18808538/twitter-kills-its-standalone-live-streaming-service-periscope",
                "https://www.benzinga.com/government/20/12/18787463/ftc-orders-social-media-giants-to-share-information-on-data-collection-policies",
                "https://www.benzinga.com/government/20/12/18788385/facebook-youtube-twitter-face-multi-billion-fines-in-uk-under-online-safety-legislation",
                "https://www.benzinga.com/markets/options/20/12/18778990/10-communication-services-stocks-with-unusual-options-alerts-in-todays-session",
                "https://www.benzinga.com/news/20/12/18774717/stocks-that-hit-52-week-highs-on-monday",
                "https://www.benzinga.com/news/20/12/18759752/5-fun-facts-you-might-not-know-about-jack-dorsey",
                "https://www.benzinga.com/markets/options/20/12/18755486/8-communication-services-stocks-with-unusual-options-alerts-in-todays-session",
                "https://www.benzinga.com/news/earnings/20/12/18752181/roce-insights-for-twitter",
                "https://www.benzinga.com/news/20/12/18717247/2020-google-trends-the-most-searched-terms-people-and-entertainment",
                "https://www.benzinga.com/news/20/12/18688461/these-were-the-most-popular-people-and-emojis-on-twitter-in-2020",
                "https://www.benzinga.com/news/20/12/18669370/facebook-to-face-antitrust-lawsuits-for-monopoly-this-week-bloomberg",
                "https://www.benzinga.com/news/20/12/18648532/trump-threatens-to-veto-defense-bill-again-as-bipartisan-deal-excludes-his-demand-for-social-media-c",
                "https://www.benzinga.com/news/20/12/18609335/trump-holds-defense-bill-hostage-to-force-section-230-repeal",
                "https://www.benzinga.com/news/20/12/18588140/nintendo-updates-switch-firmware-so-users-dont-have-to-rely-on-twitter-facebook-to-transfer-media",
                "https://www.benzinga.com/markets/options/20/11/18557031/10-communication-services-stocks-with-unusual-options-alerts-in-todays-session",
                "https://www.benzinga.com/markets/options/20/11/18535748/understanding-twitters-unusual-options-activity",
                "https://www.benzinga.com/government/20/11/18525989/french-tax-authorities-nudge-amazon-facebook-to-shell-out-digital-tax-ft",
                "https://www.benzinga.com/news/20/11/18525634/twitter-to-start-handing-out-coveted-blue-checks-again-early-next-year",
                "https://www.benzinga.com/news/20/11/18524816/pinterest-experiments-with-zoom-based-online-classes-on-its-platform",
                "https://www.benzinga.com/trading-ideas/long-ideas/20/11/18484262/will-facebook-or-twitter-stock-grow-more-by-2025",
                "https://www.benzinga.com/news/20/11/18505332/snap-introduces-tiktok-like-spotlight-video-sharing-feature",
                "https://www.benzinga.com/news/20/11/18484615/facebook-prepares-to-cozy-up-to-the-biden-administration-ft",
                "https://www.benzinga.com/stock-articles/twtr/all?page=1",
            ],
        ),
    ],
)
def test_first_page_twtr(spiderTWTR, response, expected, test_kwargs):
    r = [e.url for e in spiderTWTR.parse(response, **test_kwargs)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.benzinga.com/stock-articles/fsr/all",
            headers_dict,
            [
                "https://www.benzinga.com/news/earnings/21/03/20396144/iphone-maker-foxconn-q4-earnings-drop-yoy-miss-street-estimates",
                "https://www.benzinga.com/markets/options/21/03/20344038/10-consumer-discretionary-stocks-with-unusual-options-alerts-in-todays-session",
                "https://www.benzinga.com/news/21/03/20318761/blackrock-backed-ev-startup-aims-nasdaq-debut-via-spac-merger-bloomberg",
                "https://www.benzinga.com/news/21/03/20253113/apple-supplier-foxconn-in-talks-to-make-batteries-ev-parts-with-vietnams-vinfast-report",
                "https://www.benzinga.com/news/21/03/20193240/apple-supplier-foxconn-is-exploring-north-american-ev-manufacturing-sites",
                "https://www.benzinga.com/markets/options/21/03/20146171/10-consumer-discretionary-stocks-showing-unusual-options-activity-in-todays-session",
                "https://www.benzinga.com/markets/options/21/03/20126458/10-consumer-discretionary-stocks-showing-unusual-options-activity-in-todays-session",
                "https://www.benzinga.com/news/21/03/20099082/fisker-ceos-tweet-reveals-additional-details-for-project-pear-ev-collab",
                "https://www.benzinga.com/news/21/03/20007234/iphone-demand-drives-q1-growth-for-apple-supplier-foxconn",
                "https://www.benzinga.com/markets/options/21/03/19989221/10-consumer-discretionary-stocks-showing-unusual-options-activity-in-todays-session",
                "https://www.benzinga.com/analyst-ratings/upgrades/21/03/19985031/benzingas-top-ratings-upgrades-downgrades-for-march-3-2021",
                "https://www.benzinga.com/intraday-update/21/03/19945341/12-consumer-discretionary-stocks-moving-in-tuesdays-intraday-session",
                "https://www.benzinga.com/markets/options/21/03/19919310/10-consumer-discretionary-stocks-showing-unusual-options-activity-in-todays-session",
                "https://www.benzinga.com/intraday-update/21/03/19919253/9-consumer-discretionary-stocks-moving-in-mondays-intraday-session",
                "https://www.benzinga.com/pre-market-outlook/21/03/19911097/12-consumer-discretionary-stocks-moving-in-mondays-pre-market-session",
                "https://www.benzinga.com/news/21/03/19905983/72-biggest-movers-from-friday",
                "https://www.benzinga.com/m-a/21/02/19895980/spacs-attack-weekly-recap-looking-back-at-11-deal-announcements-new-spacs-to-watch-and-headline-news",
                "https://www.benzinga.com/markets/options/21/02/19884767/10-consumer-discretionary-stocks-with-unusual-options-alerts-in-todays-session",
                "https://www.benzinga.com/news/21/02/19872808/top-10-electric-vehicle-stocks-you-should-know-about",
                "https://www.benzinga.com/tech/21/02/19872851/fiskers-goals-go-well-beyond-simply-chipping-away-teslas-market-share-ceo",
                "https://www.benzinga.com/news/earnings/21/02/19869451/3-former-spacs-report-earnings-what-fisker-velodyne-lidar-virgin-galactic-investors-should-know",
                "https://www.benzinga.com/after-hours-center/21/02/19866857/12-consumer-discretionary-stocks-moving-in-thursdays-after-market-session",
                "https://www.benzinga.com/news/21/02/19846923/80-biggest-movers-from-yesterday",
                "https://www.benzinga.com/news/21/02/19834033/61-stocks-moving-in-wednesdays-mid-day-session",
                "https://www.benzinga.com/intraday-update/21/02/19833264/12-consumer-discretionary-stocks-moving-in-wednesdays-intraday-session",
                "https://www.benzinga.com/trading-ideas/movers/21/02/19821440/is-now-the-time-to-buy-stock-in-fisker-snap-jumia-or-fuelcell",
                "https://www.benzinga.com/news/21/02/19819624/fisker-joins-hands-with-foxconn-for-second-ev-model-what-you-need-to-know",
                "https://www.benzinga.com/pre-market-outlook/21/02/19819647/12-consumer-discretionary-stocks-moving-in-wednesdays-pre-market-session",
                "https://www.benzinga.com/markets/cryptocurrency/21/02/19733659/7-electric-vehicle-accounts-to-follow-on-twitter",
                "https://www.benzinga.com/news/21/02/19682402/43-stocks-moving-in-tuesdays-mid-day-session",
                "https://www.benzinga.com/news/21/02/19667615/64-biggest-movers-from-friday",
                "https://www.benzinga.com/analyst-ratings/analyst-color/21/02/19639961/why-morgan-stanley-is-bullish-on-quantumscape-fisker-bearish-on-lordstown-romeo-pow",
                "https://www.benzinga.com/intraday-update/21/02/19642859/12-consumer-discretionary-stocks-moving-in-fridays-intraday-session",
                "https://www.benzinga.com/news/21/02/19643341/30-stocks-moving-in-fridays-mid-day-session",
                "https://www.benzinga.com/markets/options/21/02/19642936/10-consumer-discretionary-stocks-with-unusual-options-alerts-in-todays-session",
                "https://www.benzinga.com/analyst-ratings/upgrades/21/02/19639025/benzingas-top-ratings-upgrades-downgrades-for-february-12-2021",
                "https://www.benzinga.com/stock-articles/fsr/all?page=1",
            ],
        ),
    ],
)
def test_first_page_fsr(spiderFSR, response, expected, test_kwargs):
    r = [e.url for e in spiderFSR.parse(response, **test_kwargs)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "page", "expected"],
    [
        (
            "https://www.benzinga.com/stock-articles/twtr/all?page=36",
            headers_dict,
            36,
            [
                "https://www.benzinga.com/18/07/12050830/paypal-pypl-to-post-q2-earnings-whats-in-the-offing",
                "https://www.benzinga.com/news/18/07/12042088/51-biggest-movers-from-yesterday",
                "https://www.benzinga.com/news/18/07/12038735/42-stocks-moving-in-wednesdays-mid-day-session",
                "https://www.benzinga.com/analyst-ratings/analyst-color/18/07/12037317/macquarie-downgrades-twitter-says-valuation-will-likely",
                "https://www.benzinga.com/analyst-ratings/analyst-color/18/07/12037280/munster-to-musk-apologize-ignore-the-shorts-and-maybe-t",
                "https://www.benzinga.com/analyst-ratings/upgrades/18/07/12037179/benzingas-top-upgrades-downgrades-for-july-18-2018",
                "https://www.benzinga.com/18/07/12037447/sogou-inc-sogo-catches-eye-stock-jumps-8",
                "https://www.benzinga.com/18/07/12029730/factors-setting-the-tone-for-microsofts-msft-q4-earnings",
                "https://www.benzinga.com/media/18/07/12021221/benzingas-bulls-bears-of-the-week-at-t-facebook-intel-netflix-twitter-and-more",
                "https://www.benzinga.com/stock-articles/twtr/all?page=37",
            ],
        ),
    ],
)
def test_last_page_twtr(spiderTWTR, response, page, expected, test_kwargs):
    spiderTWTR.page = page
    r = [e.url for e in spiderTWTR.parse(response, **test_kwargs)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "page", "expected"],
    [
        (
            "https://www.benzinga.com/stock-articles/fsr/all?page=2",
            headers_dict,
            2,
            [
                "https://www.benzinga.com/markets/penny-stocks/20/11/18985831/chart-setups-for-the-coming-week",
                "https://www.benzinga.com/intraday-update/20/11/18363762/12-consumer-cyclical-stocks-moving-in-fridays-intraday-session",
                "https://www.benzinga.com/news/20/11/18363851/54-stocks-moving-in-fridays-mid-day-session",
                "https://www.benzinga.com/markets/penny-stocks/20/11/18360030/cramer-says-musk-is-wrong-by-focusing-on-electric-says-hydrogen-is-great",
                "https://www.benzinga.com/pre-market-outlook/20/11/18358265/12-consumer-cyclical-stocks-moving-in-fridays-pre-market-session",
                "https://www.benzinga.com/news/20/11/18357018/46-stocks-moving-in-fridays-pre-market-session",
                "https://www.benzinga.com/news/20/11/18291957/100-biggest-movers-from-yesterday",
                "https://www.benzinga.com/analyst-ratings/analyst-color/20/11/18278643/fisker-shares-rally-on-bullish-projections-for-ev-developer",
                "https://www.benzinga.com/markets/penny-stocks/20/11/18274324/benzingas-top-upgrades-downgrades-for-november-9-2020",
                "https://www.benzinga.com/news/20/11/18221275/volvo-to-manufacture-fully-electric-heavy-duty-truck-in-2022-ft",
                "https://www.benzinga.com/news/small-cap/20/11/18199571/cramer-weighs-in-on-fisker-novocure-and-more",
                "https://www.benzinga.com/news/20/11/18196260/7-current-and-former-spacs-that-could-be-2020-election-plays",
                "https://www.benzinga.com/news/20/11/18184268/36-stocks-moving-in-tuesdays-pre-market-session",
                "https://www.benzinga.com/news/20/11/18182729/54-biggest-movers-from-yesterday",
                "https://www.benzinga.com/news/20/11/18172222/46-stocks-moving-in-mondays-mid-day-session",
                "https://www.benzinga.com/news/20/11/18163743/33-stocks-moving-in-mondays-pre-market-session",
                "https://www.benzinga.com/news/20/11/18161863/76-biggest-movers-from-friday",
                "https://www.benzinga.com/news/20/10/18144543/fisker-shares-rise-in-nyse-debut-ceo-talks-future-ev-market-on-cnbc",
                "https://www.benzinga.com/news/20/10/18135516/ev-maker-fisker-to-make-nyse-trading-debut-today-after-spac-merger",
                "https://www.benzinga.com/20/06/16341857/hartford-financial-units-get-rating-action-from-am-best",
                "https://www.benzinga.com/19/09/14398933/genworth-and-subsidiaries-get-rating-action-from-a-m-best",
                "https://www.benzinga.com/19/04/13532901/voya-financial-units-get-rating-affirmation-from-a-m-best",
                "https://www.benzinga.com/18/09/12337008/proassurance-pra-units-get-ratings-affirmed-by-a-m-best",
                "https://www.benzinga.com/stock-articles/fsr/all?page=3",
            ],
        ),
    ],
)
def test_last_page_fsr(spiderFSR, response, page, expected, test_kwargs):
    spiderFSR.page = page
    r = [e.url for e in spiderFSR.parse(response, **test_kwargs)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.benzinga.com/trading-ideas/long-ideas/18/04/11486561/benzingas-bulls-bears-of-the-week-amazon-fitbit-mattel-twitt",
            headers_dict,
        ),
    ],
)
def test_article(spiderTWTR, response, test_kwargs):
    r = next(spiderTWTR.parse_article(response, **test_kwargs))
    assert (
        r["url"]
        == "https://www.benzinga.com/trading-ideas/long-ideas/18/04/11486561/benzingas-bulls-bears-of-the-week-amazon-fitbit-mattel-twitt"
    )
    assert r["text"] == (
        "Benzinga has featured looks at many investor favorite stocks over the past "
        "week. Bullish calls included the president's recent whipping boy. "
        "Semiconductor makers featured in both bullish and bearish calls. It was a "
        "week when fears of a trade war increased and the big tech stocks remained in "
        "the glare of the spotlight. Amazon and Facebook in particular continued to "
        "see their bulls and bears squabbling over their prospects. Of course, "
        "Benzinga continued to feature looks at the prospects for many investor "
        "favorite stocks. Here are just a few of this past week's bullish and bearish "
        'posts that may be worth another look. Bulls "The Rise Of An Empire : All The '
        "Ways Amazon Grew Even Bigger Under Trump's Nose\" by Elizabeth Balboa shows "
        "how Amazon.com, Inc. (NASDAQ: AMZN ) has expanded in the past year or so. In "
        "\"Tech Strategist: Twitter Is The Main Beneficiary Of Facebook's Privacy "
        'Scandal," Brett Hershman examines how Twitter Inc (NYSE: TWTR ) has fared in '
        "the social media sector upheaval. Wayne Duggan's \"Bank Of America Adds "
        'Nvidia To Top Stock List After Latest Gaming Checks" shows that analysts '
        "remain bullish despite NVIDIA Corporation (NASDAQ: NVDA ) halting its "
        "autonomous vehicle program. Weakness in Schlumberger Limited. (NYSE: SLB ) "
        "is a buying opportunity, according to Shanthi Rexaline's \"Analyst: "
        'Schlumberger Is A Strong Oilfield Stock In Down Markets." In Jayson '
        'Derrick\'s "Citi Turns Bullish On US Steel After 25% Sell-Off," see why one '
        "top analyst sees United States Steel Corporation (NYSE: X ) as attractive "
        "now. Related link: Your Taxes And Investments In 2018: What's Changed? Bears "
        '" UBS Initiates On Semis: Intel Is Golden, Micron Is A Sell, Nvidia, AMD And '
        'More " by Wayne Duggan looks at why Micron Technology, Inc. (NASDAQ: MU ) '
        "was one of the few losers in a semiconductor sector call. In Elizabeth "
        "Balboa's \" Bernstein: 'Uncertainties Loom Ahead' For Tesla Following Q1 "
        'Delivery Report ," see what issues Tesla Inc (NASDAQ: TSLA ) now faces. New '
        "Fitbit Inc (NYSE: FIT ) initiatives are unlikely to offset declining demand "
        'and sales, according to an analyst in "3 Reasons Why Morgan Stanley Is '
        'Bearish On Fitbit " by Jayson Derrick. In "Insulation Momentum Is Already '
        'Priced Into Owens Corning , Goldman Sachs Says In Downgrade," Shanthi '
        "Rexaline shows why a prior bull has downgraded Owens Corning (NYSE: OC ). "
        "Jayson Derrick's \"Toys 'R' Us Aftershocks: Stifel Pessimistic On Hasbro, "
        'Mattel Ahead Of Q1 Prints" makes the case that Mattel, Inc. (NYSE: MAT ) has '
        'limited turnaround potential. Be sure to check out " How Close Are We To A '
        'Bear Market, And Can It Be Avoided? " as well. At the time of this writing, '
        "the author had no position in the mentioned equities. Keep up with all the "
        "latest breaking news and trading ideas by following Benzinga on Twitter. © "
        "2020 Benzinga.com. Benzinga does not provide investment advice. All rights "
        "reserved."
    )
    assert r["created_at"] == "2018-04-08T00:00:00+00:00"
    assert (
        r["title"]
        == "Benzinga's Bulls & Bears Of The Week: Amazon, Fitbit, Mattel, Twitter And More"
    )
