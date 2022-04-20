"""Test suit for Stocktwits."""

from agblox.spiders.helpers import headers
from agblox.spiders.stocktwits import StocktwitsSpider
import pytest


@pytest.fixture()
def spider():
    return StocktwitsSpider()


headers = headers(StocktwitsSpider.host_header)
headers["User-Agent"] = StocktwitsSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://api.stocktwits.com/api/2/streams/symbol/PKG.json?filter=top&limit=50",
            headers,
        ),
    ],
)
def test_last_url(spider, response, vcr_settings):
    kwargs = {
        "ticker": "PKG",
        "last_url": "https://api.stocktwits.com/api/2/streams/symbol/"
        "PKG.json?filter=top&limit=50",
    }

    r = [e["url"] for e in spider.parse(response, **kwargs)]
    assert len(r) == 0
