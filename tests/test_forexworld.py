"""Test suit for ForexWorldSpider."""

from agblox.spiders.forexworld import ForexWorldSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return ForexWorldSpider()


@pytest.fixture()
def page6Spider():
    s = ForexWorldSpider()
    s.page = 6
    return s


headers = headers(ForexWorldSpider.host_header)
headers["User-Agent"] = ForexWorldSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            ForexWorldSpider.url,
            headers,
            [
                "https://www.forexnews.world/following-the-success-of-covestings-first-five-star-trader/",
                "https://www.forexnews.world/export-retention-standardized-for-all-sectors-by-rbz/",
                "https://www.forexnews.world/dollar-moves-higher-due-to-positive-sentiments-in-the-currency-markets/",
                "https://www.forexnews.world/no-consensus-by-lawmakers-on-u-s-fiscal-package-dollar-takes-a-hit/",
                "https://www.forexnews.world/pressure-on-the-dollar-as-vaccine-hopes-rise-high/",
                "https://www.forexnews.world/euro-hovers-near-four-month-high-as-sectors-aims-at-the-eu-summit/",
                "https://www.forexnews.world/hopes-of-a-new-vaccine-pushes-the-dollar-to-a-one-month-low/",
                "https://www.forexnews.world/the-crude-oil-stocks-saw-a-rise-due-to-global-stocks-recovery/",
                "https://www.forexnews.world/wells-fargo-does-not-allow-customers-to-purchase-bitcoin/",
                "https://www.forexnews.world/ripple-invests-0-5-billion-in-xpring-to-promote-the-adoption-of-xrp/",
                "https://www.forexnews.world/iran-moots-common-cryptocurrency-for-muslim-nations-at-kuala-lumpur-2019-summit/",
                "https://www.forexnews.world/category/forex/page/2",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.forexnews.world/category/forex/page/6",
            headers,
            [
                "https://www.forexnews.world/us-probing-swedens-swedbank-ab-baltic-branch-for-violating-sanctions-on-russia/",
                "https://www.forexnews.world/dollar-takes-drastic-plunges-in-the-light-of-u-s-china-trade-war/",
                "https://www.forexnews.world/asia-pacific-stocks-get-boost-in-the-hopes-of-resolutions-of-us-china-trade-war/",
                "https://www.forexnews.world/the-central-bank-of-nigeria-sold-4-4-billion-of-foreign-exchange-to-dealers-in-april-may/",
                "https://www.forexnews.world/the-us-dollar-edges-higher-as-investors-look-for-safe-bets-ahead-of-central-bank-meets/",
                "https://www.forexnews.world/cannabis-organisation-pasha-brands-announces-its-listing-on-the-frankfurt-stock-exchange/",
                "https://www.forexnews.world/trinidad-and-tobago-mp-complains-about-unfair-foreign-exchange-distribution/",
                "https://www.forexnews.world/nigerias-ie-forex-window-brings-in-18-7-billion-in-just-seven-months-so-far/",
                "https://www.forexnews.world/neo-price-analysis-neo-down-to-14-74-will-it-manage-to-outsmart-the-bears/",
                "https://www.forexnews.world/opal-groups-public-funds-summit-2020-will-be-held-on-january-6-8-2020/",
                "https://www.forexnews.world/maruti-suzuki-partners-with-federal-bank-for-retail-car-financing-and-dealer-loans/",
                "https://www.forexnews.world/category/forex/page/7",
            ],
        ),
    ],
)
def test_last_page(page6Spider, response, expected):
    r = [e.url for e in page6Spider.parse(response)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.forexnews.world/following-the-success-of-covestings-first-five-star-trader/",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "Home Forex News Following The Success Of Covesting's First Five-Star Trader Following The Success Of Covesting’s First Five-Star Trader By David Pender October 29, 2020 0 0 Weeks ago, a challenge was put out amongst the trading community: try to become the first five-star Covesting trader. At the time, the feat hadn’t yet been accomplished, but after some of the best the world has to offer began to learn of the challenge, there are now not just one, but two of these five-star traders. Interestingly, neither have made it into the top ten by total profit, but when you dig into the success and risk metrics, and come to understand what the fully transparent five-star system truly means, the achievement becomes that much more impressive. And it also puts a spotlight on why the strategies that earn the accolades are among the safest follows on the platform. Learn all about this one ultra-successful strategy manager’s road to glory that also brought riches to their followers. What Is Covesting? A Quick Recap On The Copy Trading Platform On PrimeXBT Covesting is an innovative copy trading platform that connects traders turned strategy managers with followers looking to take the worry out and time investment out of trading and let the professionals do it for them. Followers copy the trades of strategy managers who are doing what they do best: building positions, managing risk, and trying to book profits consistently. But by becoming a strategy manager on Covesting, success fees are earned from follower equity in addition to the profits from trading, resulting in the ultimate income-generating solution. For that reason, as well as making a name for oneself on the global leaderboards that so many traders have registered and are sharing their PnL screenshots from within the platform online. After months on PrimeXBT, Covesting has amassed a substantial user base of strategy managers and followers. Single strategy managers are now trading with as much as 100 BTC in follower equity and using it to generate over 2,000% ROI. But as you can see in the list of top ten Covesting traders by total profit, there’s a notable lack of five-star traders. If even some of the greatest and most profitable traders can’t reach the stars both literally and figuratively, then how challenging is it? Reaching For The Stars: How One Strategy Manager Built Steady Success On Covesting It is achievable, as two traders have now done so. However, for months the full five stars were left unfilled until a challenge went out calling out all top traders and pushing them to give the then never-before-done feat a try. Traders lined up to give it a chance, but strategy manager Joao Strategy was the first to get the job done. To become a five-star trader, certain conditions must be met and maintained. To start, the easiest achievable star requires at least 0.5 BTC in equity. The equity can be deposited or built up from a low starting deposit and proves the strategy manager is serious about trading. Next, a trader must be active more than 30 out of 60 trading days in a rolling period. If the trader falls under 30 at any point within the current 60-day timeframe, the star will be removed. The reason for this star is to ensure any traders are active enough to warrant the follow. The third star starts to foray into safety and strict risk management. This star is awarded for keeping margin allocation at 60% or above. Traders that consistently fall below these levels are risking more capital than they should be. Any trader that has this star is a safer bet than others. Notice how Joao Strategy’s margin allocation barely ever fell below 60%. Only one spike down broke the streak of safety, but this also shows that even the safest and most consistently successful traders still are taken by surprise by unexpected moves. The fourth star requires traders to maintain a win:loss ratio of 70:30 within the last 30 trading days, which is an extremely difficult number to achieve, as almost any trader will attest to. Only the most successful of all are able to earn this star and maintain it. Joao Strategy is one of those traders. By sticking to proper risk management, only taking trades when confident, and clearly having natural technical analysis talent, they consistently grew their capital and profitability. Other profitability indicators and success metrics show how successful the strategy manager is, with full transparency. Followers can use this intel to choose the best trader to suit their needs. The fifth and final star is given to those with over 50 BTC in trading turnover over the last 30 trading days. This is no problem at all for Joao Strategy, who is now trading with over 40 BTC in capital. Notice that as soon as Joao Strategy reached the five-star rating system, their follower equity went more parabolic than Bitcoin has recently. Not only is Joao Strategy the first trader to achieve five-stars and enjoy all the fame and followers that come along with it, but they are also a great example of a community within a community brewing and the network effect and power of a peer-to-peer copy trading platform. Joao Strategy on Covesting even hosts its own Telegram channel, with more than 300 members currently. These members make up his follower base, who follows not only the trader on Covesting but also his every chart and call. By always sharing details of their trades with their followers, followers can be more comfortable in their equity in the hands of others. And when combined with the transparency of the COvesting leaderboard and the success and safety of the five-star rating system, sleeping at night gets a lot easier than compared to HODLing alone. Can You Become A Five-Star Trader With Covesting On PrimeXBT? Covesting is available on PrimeXBT , an award-winning margin trading platform where users can long and short Bitcoin -based CFDs on index trading , gold, silver, crypto, forex, and more. The platform’s professional yet easy to use trading tools are provided to Covesting strategy managers to increase profitability and minimize risk. After seeing such success unfold before your very eyes, do you have what it takes to become the next five-star trader on Covesting? David Pender David is a journalist interested in writing news-stories regarding forex. He has been in forex industry since 2014. he recently, joined our team as a news writer. He studied mass communication and has 7+ years of experience. He is an avid trader. He can be reached by email: david@forexnews.world . Previous article THINK OF AD WORLD: THINK OF GLADIO.COM"
    )
    assert r["created_at"] == "2020-10-29T11:30:03+00:00"
    assert r["tags"] == ["forex", "article", "forexnews.world"]
    assert r["title"] == "Following The Success Of Covesting’s First Five-Star Trader"
