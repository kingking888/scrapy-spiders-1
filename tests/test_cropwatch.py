"""Test suit for CropwatchsoySpider."""

from agblox.spiders.cropwatch import CropwatchSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return CropwatchSpider()


headers = headers(CropwatchSpider.host_header)
headers["User-Agent"] = CropwatchSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            CropwatchSpider.url,
            headers,
            [
                "https://cropwatch.unl.edu/2020/managing-diseases-starts-now-seed-selection",
                "https://cropwatch.unl.edu/2020/nebraska-extension-and-nebraska-soybean-board-launch-soybean-management-virtual-field-days",
                "https://cropwatch.unl.edu/2020/soybean-micronutrient-management-southeast-nebraska-chloride",
                "https://cropwatch.unl.edu/2020/usepa-approves-three-dicamba-products-five-years",
                "https://cropwatch.unl.edu/2020/soybean-micronutrient-management-southeast-nebraska-boron",
                "https://cropwatch.unl.edu/2020/nebraska-harvest-continues-ahead-average",
                "https://cropwatch.unl.edu/2020/nebraska-crop-progress-and-condition-oct-11",
                "https://cropwatch.unl.edu/2020/new-series-soybean-micronutrient-management-southeast-nebraska",
                "https://cropwatch.unl.edu/tags/soybean?page=0%2C1",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    # assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://cropwatch.unl.edu/tags/soybean?page=0%2C42",
            headers,
            [
                "https://cropwatch.unl.edu/2016/soybean-seeding-rate-tips",
                "https://cropwatch.unl.edu/2016/early-bird-gets-worm-benefits-early-soybean-planting",
                "https://cropwatch.unl.edu/2016/three-key-considerations-early-planting-corn-and-soybeans",
                "https://cropwatch.unl.edu/2016/new-soybean-web-tool-focuses-current-pest-management-tasks",
                "https://cropwatch.unl.edu/2016/ilevo%C2%AE-seed-treatment-shows-promise-sudden-death-syndrome",
                "https://cropwatch.unl.edu/2016/start-now-manage-early-weeds-your-soybean-fields",
                "https://cropwatch.unl.edu/2016/new-soybean-herbicides-2016",
                "https://cropwatch.unl.edu/soybean-planting-tips-optimal-yield-2015",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    # assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://cropwatch.unl.edu/2020/usda-nebraska-small-grain-production-and-sept-1-grain-stocks",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["text"]
        == """2020 Nebraska Small Grain Acreage and Production\nWinter wheat production is estimated at 34.0 million bushels, down 38% from last year, according to the USDA’s National Agricultural Statistics Service. The area harvested for grain totaled 830,000 acres, down 14% from 2019. Planted acreage totaled a record low 900,000, down 16% from a year earlier. The yield is 41.0 bushels per acre, down 16 bushels from last year.\nOat production is estimated at 1.83 million bushels, up 61% from 2019. Area harvested for grain, at 29,000 acres, is up 61% from last year. Planted acreage totaled 135,000, up 13% from a year earlier. Average yield is 63.0 bushels per acre, unchanged from 2019.\nNebraska September 1, 2020 Grain Stocks\nNebraska corn stocks in all positions on September 1, 2020 totaled 239 million bushels, down slightly from 2019, according to the USDA's National Agricultural Statistics Service. Of the total, 87.0 million bushels are stored on farms, up 2% from a year ago. Off-farm stocks, at 152 million bushels, are down 2% from last year.\nSoybeans stored in all positions totaled 51.2 million bushels, down 20% from last year. On-farm stocks of 14.5 million bushels are up 38% from a year ago, but off-farm stocks, at 36.7 million bushels, are down 32% from 2019.\nWheat stored in all positions totaled 52.3 million bushels, down 27% from a year ago. On-farm stocks of 4.20 million bushels are down 51% from 2019 and off-farm stocks of 48.1 million bushels are down 24% from last year.\nSorghum Off-farm holdings, at 1.06 million bushels, are down 61% from last year.\nOat stocks stored in all positions totaled 1.69 million bushels. On-farm stocks totaled 600,000 bushels, down 40% from 2019 and off-farm stocks totaled 1.09 million bushels. Barley stocks stored in all positions totaled 187,000 bushels. 2020 Crop Reports Soybean Sorghum"""
    )
    assert r["created_at"] == "2020-10-01T00:00:00+00:00"
    assert r["tags"] == ["article", "cropwatch.unl.edu"]
    assert r["title"] == "USDA: Nebraska Small Grain Production and Sept. 1 Grain Stocks"
