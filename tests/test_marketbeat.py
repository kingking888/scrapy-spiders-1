"""Test suit for Marketbeat."""

from agblox.spiders.helpers import headers
from agblox.spiders.marketbeat import MarketbeatSpider
import pytest


@pytest.fixture()
def spider():
    return MarketbeatSpider()


@pytest.fixture()
def test_kwargs():
    return {
        "ticker": "TWTR",
        "last_url": None,
        "name": "marketbeat",
        "tags": ["article", "marketbeat.com", "equity"],
    }


headers_dict = headers(MarketbeatSpider.host_header)
headers_dict["User-Agent"] = MarketbeatSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.marketbeat.com/articles/professor-quits-after-posing-as-female-immigrant-on-twitter-2021-02-12/?1",
            headers_dict,
        ),
    ],
)
def test_article(spider, response):
    r = next(
        spider.parse_article(
            response=response,
            tags=["article", "marketbeat.com", "equity"],
            name="marketbeat",
            ticker="TWTR",
        )
    )
    assert (
        r["url"]
        == "https://www.marketbeat.com/articles/professor-quits-after-posing-as-female-immigrant-on-twitter-2021-02-12/?1"
    )
    assert (
        r["text"]
        == """A white, male University of New Hampshire chemistry professor has resigned after being accused of posing as a female immigrant of color on Twitter to make racist and sexist comments. The university, which has not named the professor and described the person only as a faculty member, confirmed the resignation Friday after a four-month investigation. University President James Dean Jr. sent a letter to the community Wednesday announcing the person had resigned, a spokesperson said. The letter did not release details of the investigation. “While we are limited in what we can say in order to protect the privacy of all involved, we can share that the faculty member chose to resign when the university concluded that the conduct exhibited was not consistent with the university’s values and our expectation that every faculty member contribute to a professional academic environment free of intimidation and harassment,” Dean wrote. The chair of the university’s chemistry department, Glen Miller, did not respond to a request for comment Friday. But in an October email previously obtained by The Associated Press, Miller used the white, male professor's first name and acknowledged the professor had set up a Twitter account as an impostor with tweets that ranged from “unfortunate to hurtful to deeply offensive.” Emails seeking comment that were sent to the university email account believed to be the professor's were not returned but did not bounce back, and a phone number for him could not be found. Several people who reviewed the account before it was taken down late last year said it routinely contained racist, sexist and transphobic comments and images. The person behind the account also detailed fighting efforts from an unnamed police department to speak out on racial injustice following the police killing of George Floyd. The person also routinely mentioned a fake background to criticize users who were pushing for greater diversity in science, mathematics, engineering and technology. Several people also accused the user of attacking mostly women of color who disagreed and encouraging his followers to do the same. Toby SantaMaria, a graduate student studying plant biology at Michigan State who identifies with the gender-neutral term Latinx and was attacked online by followers of the Twitter account, welcomed the professor's resignation. “Pretending to be a woman on the internet explicitly to bully, shame, harass, and create toxic spaces against POC deserves heavy consequences," they said in an email interview, referring to people of color. "It deserves heavy consequences because it shows a deep seated bias against historically excluded groups. If you are a professor, teaching POC, that kind of racism and misogyny is unacceptable.”"""
    )
    assert r["created_at"] == "2021-02-12T00:00:00+00:00"
    assert r["tags"] == ["article", "marketbeat.com", "equity", "TWTR"]
    assert r["title"] == "Professor quits after posing as female immigrant on Twitter"


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.marketbeat.com/instant-alerts/nyse-rcus-volume%20advance-2021-04-2-3/",
            headers_dict,
        ),
    ],
)
def test_text_processing(spider, response, test_kwargs):
    r = next(spider.parse_article(response=response, **test_kwargs))
    assert (
        r["url"]
        == "https://www.marketbeat.com/instant-alerts/nyse-rcus-volume%20advance-2021-04-2-3/"
    )

    assert (
        r["text"] == "Shares of Arcus Biosciences, Inc. (NYSE:RCUS) saw strong trading volume on "
        "Tuesday after an insider bought additional shares in the company. 25,002 "
        "shares were traded during mid-day trading, a decline of 95% from the "
        "previous session's volume of 534,409 shares.The stock last traded at $34.38 "
        "and had previously closed at $35.68.Specifically, Director Kathryn E. "
        "Falberg purchased 20,000 shares of the firm's stock in a transaction on "
        "Wednesday, March 31st. The stock was bought at an average cost of $28.35 per "
        "share, with a total value of $567,000.00. Following the completion of the "
        "acquisition, the director now owns 80,504 shares of the company's stock, "
        "valued at approximately $2,282,288.40. The transaction was disclosed in a "
        "document filed with the Securities & Exchange Commission, which is "
        "accessible through . Also, Director Yasunori Kaneko purchased 4,133 shares "
        "of the firm's stock in a transaction on Friday, April 23rd. The stock was "
        "bought at an average cost of $31.37 per share, with a total value of "
        "$129,652.21. Following the completion of the acquisition, the director now "
        "directly owns 6,717 shares of the company's stock, valued at approximately "
        "$210,712.29. The disclosure for this purchase can be found . Insiders have "
        "purchased 5,674,133 shares of company stock valued at $221,046,652 in the "
        "last ninety days. Corporate insiders own 19.71% of the company's stock. "
        "Several research analysts have recently weighed in on RCUS shares. Cantor "
        "Fitzgerald upped their target price on Arcus Biosciences from $39.00 to "
        '$62.00 and gave the stock an "overweight" rating in a research note on '
        "Wednesday, January 13th. SVB Leerink reduced their target price on Arcus "
        'Biosciences from $54.00 to $53.00 and set an "outperform" rating for the '
        "company in a research note on Wednesday, March 3rd. Wedbush upped their "
        "target price on Arcus Biosciences from $48.00 to $55.00 and gave the stock "
        'an "outperform" rating in a research note on Tuesday, January 19th. Barclays '
        "boosted their price target on Arcus Biosciences from $40.00 to $45.00 and "
        'gave the stock an "overweight" rating in a research report on Thursday, '
        'February 25th. Finally, upgraded Arcus Biosciences from a "sell" rating to a '
        '"hold" rating in a report on Thursday, March 4th. One investment analyst has '
        "rated the stock with a hold rating and nine have issued a buy rating to the "
        "company's stock. Arcus Biosciences presently has a consensus rating of "
        '"Buy" and an average price target of $49.73. The company has a market '
        "capitalization of $2.45 billion, a price-to-earnings ratio of -18.68 and a "
        "beta of 1.26. The stock has a fifty day moving average price of $33.20 and a "
        "two-hundred day moving average price of $30.20. Arcus Biosciences "
        "(NYSE:RCUS) last released its quarterly earnings results on Tuesday, "
        "February 23rd. The company reported ($0.82) earnings per share for the "
        "quarter, missing the Zacks' consensus estimate of ($0.74) by ($0.08). The "
        "company had revenue of $9.49 million during the quarter, compared to analyst "
        "estimates of $15.35 million. Arcus Biosciences had a negative return on "
        "equity of 27.43% and a negative net margin of 112.63%. Equities research "
        "analysts predict that Arcus Biosciences, Inc. will post -1.95 earnings per "
        "share for the current year. A number of hedge funds have recently bought and "
        "sold shares of RCUS. California State Teachers Retirement System grew its "
        "position in Arcus Biosciences by 29.3% during the third quarter. California "
        "State Teachers Retirement System now owns 63,790 shares of the company's "
        "stock valued at $1,093,000 after acquiring an additional 14,474 shares "
        "during the period. Pacer Advisors Inc. lifted its stake in shares of Arcus "
        "Biosciences by 19.4% in the fourth quarter. Pacer Advisors Inc. now owns "
        "2,079 shares of the company's stock worth $54,000 after acquiring an "
        "additional 338 shares in the last quarter. Strs Ohio raised its stake in "
        "Arcus Biosciences by 46.9% during the fourth quarter. Strs Ohio now owns "
        "18,800 shares of the company's stock valued at $488,000 after buying an "
        "additional 6,000 shares in the last quarter. Nisa Investment Advisors LLC "
        "bought a new position in shares of Arcus Biosciences during the fourth "
        "quarter valued at approximately $64,000. Finally, Zurcher Kantonalbank "
        "Zurich Cantonalbank boosted its stake in Arcus Biosciences by 146.9% during "
        "the 4th quarter. Zurcher Kantonalbank Zurich Cantonalbank now owns 7,797 "
        "shares of the company's stock valued at $202,000 after purchasing an "
        "additional 4,639 shares in the last quarter. 60.56% of the stock is owned by "
        "hedge funds and other institutional investors. ( ) Arcus Biosciences, Inc, a "
        "clinical-stage biopharmaceutical company, develops and commercializes cancer "
        "therapies in the United States. Its product pipeline includes, Etrumadenant, "
        "a dual A2a/A2b adenosine receptor antagonist, which is in a Phase 1b/2 "
        "clinical trial; and Zimberelimab, an anti-PD-1 antibody that is in Phase 1b "
        "clinical trial for monotherapy."
    )
