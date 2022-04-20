"""Test suit for CNBCSpider."""

from agblox.spiders.cnbc import BaseCNBCSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    s = BaseCNBCSpider()
    s.tags = ["article", "cnbc.com", "equity"]
    s.url = "https://www.cnbc.com/search/?query=TLRY&qsearchterm=TLRY"
    s.name = "cnbc-tlry"
    s.last_url = None
    return s


@pytest.fixture()
def test_kwargs():
    return {
        "ticker": "TLRY",
        "last_url": None,
        "url": "https://www.cnbc.com/search/?query=TLRY&qsearchterm=TLRY",
        "name": "cnbc-tlry",
        "tags": ["article", "cnbc.com", "equity"],
    }


headers_dict = headers(BaseCNBCSpider.host_header)
headers_dict["User-Agent"] = BaseCNBCSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.cnbc.com/2021/03/31/stocks-making-the-biggest-moves-midday-walgreens-blackberry-applied-materials-more.html?&qsearchterm=TLRY",
            headers_dict,
        ),
    ],
)
def test_article(spider, response, test_kwargs):
    r = next(spider.parse_article(response, **test_kwargs))
    assert (
        r["url"]
        == "https://www.cnbc.com/2021/03/31/stocks-making-the-biggest-moves-midday-walgreens-blackberry-applied-materials-more.html?&qsearchterm=TLRY"
    )
    assert (
        r["text"]
        == """In this article MS A woman on an escalator in a Walgreens store in New York. Scott Mlyn | CNBC Check out the companies making headlines in midday trading. Walgreens — The drugstore company's shares rose 6.7% after beating analysts' expectations for its quarterly earnings. Walgreens earned $1.40 per share, topping estimates by 29 cents, according to Refinitiv. Walgreens also said it has administered 8 million Covid-19 vaccines so far and hiked its 2021 profit forecast. BlackBerry — Shares of the communications software company tumbled more than 9% following a quarterly revenue miss amid lower demand for the company's QNX care software. However, BlackBerry adjusted quarterly earnings of 3 cents per share, which matched Refinitiv's estimate. Applied Materials , Lam Research — Applied Materials climbed 5% and Lam Research popped nearly 4% after Bernstein initiated coverage on both stocks with an outperform rating. "Over the longer term we believe semiconductor capital equipment is likely to be extremely structurally advantaged, with growth trends in the underlying semi market likely to remain positive over the long term, and with a strong case to be made for semiconductor capital intensity to continue evolving higher over time...," the firm wrote in a note to clients. Bernstein's price forecast for Applied Materials and Lam Research are $160 and $700, respectively. Harley-Davidson — The motorcycle stock jumped 6.3% after investment firm Baird upgraded the stock to outperform from neutral. Baird said in a note to clients that it was bullish on retail demand for the company and believed that there were inventory shortages at dealers. Chewy — The pet supply retailer's stock jumped more than 7% after the company reported a surprise profit fir its latest quarter. Chewy reported earnings of of 5 cents per share, compared to expectations of a 10 cents per share loss, according to Refinitiv. Revenue also topped estimates as stuck-at-home consumers increased their orders of pet products. Tilray , Canopy Growth, Aphria , Aurora Cannabis — Several stocks of cannabis companies gained on Wednesday after New York passed a bill to approve the recreational use of marijuana. Gov. Andrew Cuomo signed the bill today . Tilray rose 4.5% and Canopy Growth gained 2.3%. Aphria climbed 5.5%, and Aurora Cannabis added 4.2%. Cleveland-Cliffs — The steel producer's shares surged nearly 15% in midday trading after it announced preliminary results for the quarter that ends today. The projected earnings for the quarter and the full year are well above current Wall Street projections. Apple — Apple shares rose about 2.8% in midday trading after UBS upgraded the stock to a buy rating from a neutral rating and said it expects more stable long-term iPhone demand and stronger average sales prices. The brokerage hiked its price target on Apple shares to $142 from $115, implying 18% upside from Tuesday's close. – CNBC's Maggie Fitzgerald, Jesse Pound, Pippa Stevens, and Yun Li contributed reporting."""
    )
    assert r["created_at"] == "2021-03-31T16:15:46+0000"
    assert (
        r["title"]
        == "Stocks making the biggest moves midday: Walgreens, BlackBerry, Applied Materials & more"
    )
    assert r["meta"]["base_ticker"] == "TLRY"
