"""Test suit for MarketScreener."""

from agblox.spiders.helpers import headers
from agblox.spiders.marketscreener import MarketScreenSpider
import pytest


@pytest.fixture()
def spider():
    return MarketScreenSpider()


@pytest.fixture()
def test_kwargs():
    return {"ticker": "TWTR", "last_url": None}


headers = headers(MarketScreenSpider.host_header)
headers["User-Agent"] = MarketScreenSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news-history/",
            headers,
            [
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-to-Issue-1-25-Billion-Convertible-Notes-Offering-32572068/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-Inc-nbsp-Announces-1-25-Billion-Convertible-Notes-Offering-32570490/",
                "https://www.marketscreener.com/quote/stock/PINTEREST-INC-57086058/news/Pinterest-nbsp-ICTA-Announced-Advertisement-Ban-On-Pinterest-Twitter-And-Periscope-32569532/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Canaccord-Genuity-Adjusts-Price-Target-on-Twitter-to-82-From-65-Maintains-Hold-Rat-32554559/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Rosenblatt-Adjusts-Price-Target-on-Twitter-to-65-From-55-Maintains-Neutral-Rating-32554538/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-JP-Morgan-Adjusts-Twitter-s-Price-Target-to-91-From-77-Maintains-Overweight-Rating-32552758/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Morgan-Stanley-Adjusts-Twitter-s-Price-Target-to-75-From-54-Maintains-Equal-Weight-32552739/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Mizuho-Adjusts-Twitter-s-Price-Target-to-67-From-57-Maintains-Neutral-Rating-32552726/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Goldman-Sachs-Adjusts-Twitter-s-Price-Target-to-112-From-78-Reiterates-Buy-Rating-32552725/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Jefferies-Adjusts-Twitter-s-Price-Target-to-79-From-64-Reiterates-Hold-Rating-32552719/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Piper-Sandler-Adjusts-Twitter-s-Price-Target-to-71-From-61-Maintains-Neutral-Ratin-32552718/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Pivotal-Research-Adjusts-Twitter-s-Price-Target-to-95-From-77-25-on-2023-Revenue-Fo-32551472/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-KeyBanc-Adjusts-Twitter-s-Price-Target-to-90-From-80-Keeps-Overweight-Rating-32551220/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Prepared-Remarks-32546856/",
                "https://www.marketscreener.com/quote/index/DJ-INDUSTRIAL-4945/news/US-Stocks-Finish-Sharply-Lower-as-Treasury-Yields-Climb-32545125/",
                "https://www.marketscreener.com/quote/index/DJ-INDUSTRIAL-4945/news/Close-Update-US-Stocks-Finish-Sharply-Lower-as-Treasury-Yields-Climb-32545113/",
                "https://www.marketscreener.com/quote/stock/BEST-BUY-CO-INC-11778/news/Best-Buy-Domino-s-fall-Twitter-Smucker-rise-32544342/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-Aims-to-Double-Revenue-by-2023-Update-32543685/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Street-Color-Twitter-Exploring-Monetary-Incentives-Like-Tipping-and-Account-Subscriptions-by-Super-32543127/",
                "https://www.marketscreener.com/quote/index/NASDAQ-100-4946/news/Midday-Report-US-Stocks-Fall-While-Yields-Extend-Gains-to-Year-High-Economists-Cast-Aspersion-on-P-32542698/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Plans-to-At-Least-Double-Revenue-by-2023-as-User-Growth-Climbs-Amid-Pandemic-Led-Enga-32542205/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Sets-Goal-of-Doubling-Revenue-Hitting-315-Million-Users-by-2023-Shares-Higher-32541388/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Should-you-invest-in-Bank-of-America-Carnival-Corp-Twitter-Fisker-or-Plug-Power-32541112/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Aims-to-Double-Revenue-by-2023-32540850/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/TWITTER-INC-nbsp-Regulation-FD-Disclosure-form-8-K-32539176/",
                "https://www.marketscreener.com/quote/stock/FACEBOOK-INC-10547141/news/Facebook-nbsp-WhatsApp-and-Twitter-Face-New-Rules-in-India-32536377/",
                "https://www.marketscreener.com/quote/index/NASDAQ-COMP-4944/news/Tech-Up-As-Sector-Rebounds-From-Recent-Selloff-Tech-Roundup-32531864/",
                "https://www.marketscreener.com/quote/commodity/LONDON-SUGAR-16175/news/Coke-Whirlpool-Keep-Tax-Court-Losses-Off-the-Books-32525579/",
                "https://www.marketscreener.com/quote/stock/SQUARE-INC-24935553/news/Square-Doubling-Down-on-Bitcoin-in-2021-Growth-Plans-After-Cryptocurrency-Underpins-Fourth-Quarter-R-32524485/",
                "https://www.marketscreener.com/news/latest/Square-puts-skin-in-the-game-with-170-million-more-in-bitcoin-buy--32521359/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Disclosing-networks-of-state-linked-information-operations-32518122/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Baird-Adjusts-Price-Target-on-Twitter-to-75-From-65-Maintains-Neutral-Rating-32507814/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Insider-Sale-at-Twitter-TWTR-Continues-Selling-Trend-32489128/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Insider-Trends-Twitter-Insider-Exercises-Options-Extending-90-Day-Buying-Trend-32488529/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/TWITTER-INC-nbsp-Change-in-Directors-or-Principal-Officers-form-8-K-32487387/",
                "https://www.marketscreener.com/quote/stock/FACEBOOK-INC-10547141/news/Street-Color-White-House-Begins-Working-With-Facebook-Twitter-and-Google-to-Address-COVID-Misinfo-32484944/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Q4-2020-Fact-Sheet-32478179/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Insider-Trends-Twitter-Insider-Sale-Interrupting-90-Day-Buy-Trend-32477696/",
                "https://www.marketscreener.com/quote/index/DJ-INDUSTRIAL-4945/news/Stocks-End-Mixed-After-Strong-Retail-Sales-Report-Verizon-Chevron-Lift-Dow-to-Record-High-32466656/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/TWITTER-nbsp-MANAGEMENT-S-DISCUSSION-AND-ANALYSIS-OF-FINANCIAL-CONDITION-AND-RESULTS-OF-OPERATIONS-32466154/",
                "https://www.marketscreener.com/quote/index/DJ-INDUSTRIAL-4945/news/Close-Update-Stocks-End-Mixed-After-Strong-Retail-Sales-Report-Verizon-Chevron-Lift-Dow-to-Record-32465927/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-to-Present-at-the-J-P-Morgan-Global-High-Yield-Leveraged-Finance-Virtual-Conferenc-32465552/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Market-Chatter-Twitter-Said-to-Cut-Annual-Employee-Bonuses-After-Missing-Internal-Revenue-Profit-G-32465004/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Loop-Capital-Adjusts-Twitter-s-Price-Target-to-95-From-56-Reiterates-Buy-Rating-32454005/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Should-you-invest-in-Apple-Tilray-General-Electric-Bank-of-America-or-Twitter-32429359/",
                "https://www.marketscreener.com/quote/stock/FACEBOOK-INC-10547141/news/How-to-Quiet-the-Megaphones-of-Facebook-Google-and-Twitter-32421401/",
                "https://www.marketscreener.com/quote/stock/AUTODESK-INC-40246776/news/CFOs-Hesitate-to-Invest-in-Handle-Bitcoin-Due-to-Volatility-32420493/",
                "https://www.marketscreener.com/news/latest/GLOBAL-MARKETS-LIVE-Astrazeneca-Uber-Microsoft--32420065/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-MoffettNathanson-Upgrades-Twitter-to-Neutral-From-Sell-Price-Target-is-55-32418578/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Insiders-Make-Significant-Stock-Sales-in-Twitter-TWTR-Shares-Extending-the-Trend-of-32413368/",
                "https://www.marketscreener.com/quote/stock/ALTERYX-INC-34336524/news/Twitter-Under-Armour-rise-Alteryx-Assurant-fall-32410941/",
                "https://www.marketscreener.com/quote/stock/ALTERYX-INC-34336524/news/Sector-Update-Tech-Stocks-Ending-Lower-Despite-Narrow-Rise-by-Chipmakers-32410668/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Susquehanna-Adjusts-Twitter-s-Price-Target-to-70-From-58-Maintains-Positive-Rating-32410169/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Stifel-Adjusts-Twitter-s-Price-Target-to-60-From-50-Maintains-Hold-Rating-32410164/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Truist-Adjusts-Twitter-s-Price-Target-to-64-From-43-Maintains-Hold-Rating-32410162/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Revenue-Outlook-for-2021-Mobile-App-Promotion-Rollout-Underpins-Price-Target-Raise-a-32410048/",
                "https://www.marketscreener.com/quote/index/DJ-INDUSTRIAL-4945/news/Wall-Street-Wavers-in-Choppy-Midday-Trading-After-Inflation-Data-to-Stem-Recent-Rally-to-Record-Leve-32409884/",
                "https://www.marketscreener.com/quote/index/DJ-INDUSTRIAL-4945/news/Midday-Report-Wall-Street-Wavers-Midday-After-Recent-Rally-32409827/",
                "https://www.marketscreener.com/quote/stock/CERIDIAN-HCM-HOLDING-INC-43133651/news/Sector-Update-Narrow-Declines-for-Technology-Stocks-32409826/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Cowen-Co-Adjusts-Twitter-PT-to-58-From-48-Maintains-Market-Perform-Rating-32409634/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Q4-Results-Driven-Higher-by-Advertising-Revenue-Pivotal-Research-Says-32409475/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Growth-Across-The-Board-Drove-Twitter-Q4-Results-Wedbush-Says-32409278/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-JP-Morgan-Adjusts-Twitter-s-Price-Target-to-77-from-65-Keeps-Overweight-Rating-32409146/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Rosenblatt-Adjusts-Twitter-s-Price-Target-to-55-from-39-Keeps-Neutral-Rating-32409147/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-MKM-Partners-Adjusts-Twitter-s-Price-Target-to-73-from-60-Keeps-Buy-Rating-32409148/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Oppenheimer-Adjusts-Twitter-PT-to-70-From-58-Maintains-Outperform-Rating-32408980/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-BofA-Securities-Adjusts-Twitter-s-Price-Objective-to-78-From-58-Reiterates-Buy-Rat-32409118/",
                "https://www.marketscreener.com/news/latest/GLOBAL-MARKETS-LIVE-Cisco-Lyft-Twitter--32408735/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Sector-Update-Tech-Stocks-Gain-Premarket-Wednesday-32407734/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Sector-Update-Tech-32407363/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-UBS-Adjusts-Twitter-s-Price-Target-to-60-From-52-Maintains-Neutral-Rating-32407342/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Deutsche-Bank-Adjusts-Twitter-s-Price-Target-to-76-From-65-Maintains-Buy-Rating-32407332/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Morgan-Stanley-Adjusts-Twitter-s-Price-Target-to-54-From-50-Maintains-Equal-Weight-32407324/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Mizuho-Adjusts-Twitter-s-Price-Target-to-57-From-48-Maintains-Neutral-Rating-32407311/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-nbsp-Goldman-Sachs-Adjusts-Twitter-s-Price-Target-to-78-From-55-Reiterates-Buy-Rating-32407298/",
                "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news-history/&nbstrat=0&&fpage=2",
            ],
        ),
    ],
)
def test_first_page(spider, response, test_kwargs, expected):
    r = [e.url for e in spider.parse(response=response, **test_kwargs)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.marketscreener.com/quote/stock/TWITTER-38965267/news/Twitter-Inc-nbsp-Announces-1-25-Billion-Convertible-Notes-Offering-32570490/",
            headers,
        ),
    ],
)
def test_article(spider, response, test_kwargs):
    r = next(spider.parse_article(response=response, **test_kwargs))
    assert (
        r["text"]
        == """SAN FRANCISCO , March 1, 2021 /PRNewswire/ -- Twitter, Inc. (NYSE: TWTR) today announced its intention to offer, subject to market conditions and other factors, $1.25 billion aggregate principal amount of convertible senior notes due in 2026 (the "notes") in a private placement to qualified institutional buyers pursuant to Rule 144A under the Securities Act of 1933, as amended (the "Act"). Twitter also expects to grant the initial purchasers of the notes a 13-day option to purchase up to an additional $187.5 million aggregate principal amount of the notes, to cover over-allotments, if any.\nThe notes will be unsecured, senior obligations of Twitter, and interest will be payable semi-annually in arrears. The notes will be convertible into cash, shares of Twitter's common stock, or a combination thereof, at Twitter's election. The interest rate, initial conversion rate and other terms of the notes are to be determined upon pricing of the offering.\nIn connection with the pricing of the notes, Twitter expects to enter into privately negotiated convertible note hedge transactions with one or more of the initial purchasers or their affiliates or other financial institutions (the "hedge counterparties"). The convertible note hedge transactions are expected generally to reduce the potential dilution to the common stock upon any conversion of notes and/or offset the cash payments Twitter is required to make in excess of the principal amount of converted notes in the event that the market price of the common stock is greater than the strike price of those convertible note hedge transactions. Twitter also expects to enter into privately negotiated warrant transactions with the hedge counterparties. The warrant transactions would separately have a dilutive effect to the extent that the market value per share of common stock exceeds the strike price of any warrant transactions, unless Twitter elects, subject to certain conditions set forth in the related warrant confirmations, to settle the warrant transactions in cash. If the initial purchasers exercise their over-allotment option to purchase additional notes, Twitter intends to enter into additional convertible note hedge transactions and additional warrant transactions with the hedge counterparties.\nTwitter expects that in connection with establishing their initial hedge of the convertible note hedge transactions and warrant transactions, the hedge counterparties or their respective affiliates may purchase shares of the common stock and/or enter into various derivative transactions with respect to the common stock concurrently with, or shortly after, the pricing of the notes. These activities could increase (or reduce the size of any decrease in) the market price of Twitter's common stock or the notes at that time. In addition, Twitter expects that the hedge counterparties or their respective affiliates may modify their hedge positions by entering into or unwinding derivative transactions with respect to the common stock and/or by purchasing or selling shares of the common stock or other securities of Twitter in secondary market transactions following the pricing of the notes and prior to the maturity of the notes (and are likely to do so during any observation period relating to a conversion of the notes or in connection with any repurchase of notes by Twitter). This activity could also cause or avoid an increase or a decrease in the market price of the common stock or the notes, which could affect the ability of noteholders to convert the notes and, to the extent the activity occurs during any observation period related to a conversion of the notes, could affect the amount and value of the consideration that noteholders will receive upon conversion of the notes.\nTwitter expects to use a portion of the net proceeds from this offering to pay the cost of the convertible note hedge transactions described above (after such cost is partially offset by the proceeds to Twitter from the warrant transactions described above), and the remaining proceeds to pay any amounts due upon conversion or at maturity of its 1.00% Convertible Senior Notes due 2021 and for general corporate purposes, including capital expenditures, working capital and potential acquisitions.\nThe notes will be offered to qualified institutional buyers pursuant to Rule 144A under the Act. Neither the notes nor the shares of common stock issuable upon conversion of the notes, if any, have been, nor will be, registered under the Act or the securities laws of any other jurisdiction and may not be offered or sold in the United States absent registration or an applicable exemption from such registration requirements.\nThis announcement is neither an offer to sell nor a solicitation of an offer to buy any of these securities and shall not constitute an offer, solicitation, or sale in any jurisdiction in which such offer, solicitation, or sale is unlawful.\nPress:\nInvestors: ir@twitter.com\nPress: press@twitter.com\nView original content: http://www.prnewswire.com/news-releases/twitter-inc-announces-1-25-billion-convertible-notes-offering-301237228.html\nSOURCE Twitter, Inc."""
    )
    assert r["created_at"] == "2021-03-01T07:01:13-05:00"
    assert r["tags"] == ["equity", "marketscreener", "article", "TWTR"]
    assert r["title"] == "Twitter, Inc. : Announces $1.25 Billion Convertible Notes Offering"
