"""Test suit for Gurufocus."""
from agblox.spiders.gurufocus import GurufocusBaseSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return GurufocusBaseSpider()


@pytest.fixture()
def test_kwargs():
    return {
        "ticker": "TWTR",
        "last_url": None,
        "url": "https://www.gurufocus.com/stock/TWTR/article",
        "name": "gurufocus-twtr",
        "tags": ["TWTR", "article", "gurufocus.com"],
    }


_headers = headers(GurufocusBaseSpider.name)
_headers["User-Agent"] = GurufocusBaseSpider.user_agent
del _headers["Host"]


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        ("https://www.gurufocus.com/news/779572/weekly-cfo-sells-highlight", _headers),
    ],
)
def test_article(spider, response, test_kwargs):
    r = next(spider.parse_article(response, **test_kwargs))
    assert r["url"] == "https://www.gurufocus.com/news/779572/weekly-cfo-sells-highlight"
    assert (
        r["text"]
        == """According to GuruFocus Insider Data, the recent CFO sells were: Twitter Inc. ( NYSE:TWTR ), Tableau Software Inc. ( NYSE:DATA ) and Facebook Inc. ( NASDAQ:FB ).\nTwitter Inc. ( NYSE:TWTR ): CFO Ned D. Segal sold 6,000 shares\nCFO Ned D. Segal sold 6,000 shares for $32.16 per share on Nov. 13. Since then, the stock price has decreased by 2.21%. Twitter Inc. has a market cap of $23.94 billion and its shares were traded around $31.45. The company has a P/E ratio of 23.30 and P/S ratio of 8.38.\nTwitter announced its third-quarter results with revenue of $758.11 million and gross profit of $514.47 million, while the net income was $789.18 million. The 2017 total revenue was $2.44 billion, a 3% decrease from 2016. The 2017 gross profit was $1.58 billion, a 4% decrease from the year prior. The 2017 net loss was $108.06 million.\nWarning! GuruFocus has detected 6 Warning Signs with TWTR. Click here to check it out.\nTWTR 30-Year Financial Data The intrinsic value of TWTR Peter Lynch Chart of TWTR Director Evan Clark Williams sold 3,076,923 shares for $31.59 per share on Nov. 30. Since then, the stock price has decreased by 0.44%. VP, Engineering Michael Montano sold 1,250 shares for $30.2 per share on Nov. 20. Since then, the stock price has increased by 4.14%. Chief Accounting Officer Robert Kaiden sold 3,702 shares for $34.37 per share on Nov. 06. Since then, the stock price has decreased by 8.5%.\nTableau Software Inc. ( NYSE:DATA ): CFO Damon A Fletcher sold 2,019 shares\nCFO Damon A. Fletcher ssold 2,019 shares for $103.92 per share on Nov. 20. Since then, the stock price has increased by 19.94%. Tableau Software Inc. has a market cap of $10.42 billion and its shares were traded around $124.64. The company has a P/S ratio of 9.52.\nTableau Software announced its third-quarter results with revenue of $290.58 million and gross profit of $255.80 million, while the net loss was $21.38 million. The 2017 total revenue was $877.06 million, a 6% increase from 2016. The 2017 gross profit was $763.50 million, a 5% increase from the year prior. The 2017 net loss was $185.56 million.\nPresident and CEO Adam Selipsky sold 21,300 shares for $121.23 per share on Nov. 29. Since then, the stock price has increased by 2.81%. Director A Brooke Seawell sold 649 shares for $118.54 per share on Nov. 28. Since then, the stock price has increased by 5.15%. Director William Bosworth sold 324 shares for $111.32 per share on Nov. 26. Since then, the stock price has increased by 11.97%. Co-Founder and Technical Advisor Chris Stolte sold 95,000 shares for $110.96 per share on Nov. 26. Since then, the stock price has increased by 12.33%.\nFacebook Inc. ( NASDAQ:FB ): CFO David M. Wehner sold 4,761 shares\nCFO David M. Wehner sold 4,761 shares for $141.1 per share on Nov. 16. Since then, the stock price has decreased by 0.35%. Facebook Inc. has a market cap of $404.08 billion and its shares were traded around $140.61. The company has a P/E ratio of 21.21 and P/S ratio of 7.96. Over the past 5 years, Facebook Inc. had an annual average earnings growth of 63.50%.\nFacebook announced its third-quarter results with revenue of $13.73 billion and gross profit of $11.31 billion, while the net income was $5.14 billion. The 2017 total revenue was $40.65 billion, a 47% increase from 2016. The 2017 gross profit was $35.20 billion, a 48% increase from the year prior. The 2017 net income was $15.93 billion.\nChief Accounting Officer Susan J.S. Taylor sold 2,268 shares for $135.81 per share on Nov. 27. Since then, the stock price has increased by 3.53%. COO Sheryl Sandberg sold 55,000 shares for $135.12 per share on Nov. 27. Since then, the stock price has increased by 4.06%. Chief Technology Officer Michael Todd Schroepfer sold 38,185 shares for $135.89 per share on Nov. 21. Since then, the stock price has increased by 3.47%.\nDisclosure: None."""
    )
    assert r["created_at"] == "2018-12-02T00:00:00+00:00"
    assert r["title"] == "Weekly CFO Sells Highlight"
    assert r["tags"] == ["TWTR", "article", "gurufocus.com"]
    assert r["meta"]["base_ticker"] == "TWTR"
