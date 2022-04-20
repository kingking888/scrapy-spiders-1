"""Test suit for GrowersPointSpider."""

from agblox.spiders.growerspoint import GrowerspointSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return GrowerspointSpider()


headers_dict = headers(GrowerspointSpider.host_header)
headers_dict["User-Agent"] = GrowerspointSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            GrowerspointSpider.url,
            headers_dict,
            [
                "https://growerspoint.com/first-commercial-shipment-of-u-s-rice-unloads-in-china-from-adm-rice/",
                "https://growerspoint.com/nexusbioag-launches-next-generation-pulse-cereal-and-soybean-inoculants/",
                "https://growerspoint.com/usda-releases-wheat-outlook-report-7/",
                "https://growerspoint.com/viterra-announces-plans-for-new-elevator-in-west-central-saskatchewan/",
                "https://growerspoint.com/farmers-benefit-from-50-years-of-pioneer-wheat-breeding/",
                "https://growerspoint.com/bioceres-crop-solutions-corp-announces-regulatory-approval-of-drought-tolerant-hb4-wheat/",
                "https://growerspoint.com/grain-storage-in-alberta/",
                "https://growerspoint.com/valent-u-s-a-announces-new-zeltera-rice-system-for-fall-season/",
                "https://growerspoint.com/seasonality-of-feed-barley-prices/",
                "https://growerspoint.com/u-s-wheat-associates-introduces-interactive-wheat-export-supply-system-map/",
                "https://growerspoint.com/category/crops/wheat/page/2/",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://growerspoint.com/category/crops/wheat/page/19/",
            headers_dict,
            [
                "https://growerspoint.com/wheat-trend-is-sharply-higher-stay-long-buy-hard-set-backs/",
                "https://growerspoint.com/july-kc-wheat-sending-buy-signals/",
                "https://growerspoint.com/wheat-blew-through-resistance-buy-any-dip-with-stops-under-the-gap/",
                "https://growerspoint.com/cortevas-opensky-herbicide-receives-federal-registration/",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://growerspoint.com/amvac-releases-new-logos-for-recently-acquired-herbicides/",
            headers_dict,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["url"]
        == "https://growerspoint.com/amvac-releases-new-logos-for-recently-acquired-herbicides/"
    )
    assert r["text"] == (
        "AgNewsWire reports:\nProvides preemergence and postemergence control of key "
        "broadleaf weeds in soybeans.\nNewport Beach, CA – AMVAC, an American Vanguard "
        "company, has designed new product logos and web pages for its recently acquired "
        "herbicides: Classic Herbicide, FirstRate Herbicide, Hornet Herbicide and Python "
        "Herbicide.\nExpands postemergence weed control spectrum in soybeans.\n“We are "
        "excited to offer these herbicide brands from AMVAC, expanding our crop protection "
        "portfolio and offering growers additional trusted solutions,” said Nathaniel Quinn, "
        "marketing manager for corn, soybean and sugar beet. “These products have been a key "
        "component to growers’ operations for many years, and we are pleased to offer these "
        "trusted solutions now with a refreshed brand image.”\nDelivers postemergence "
        "broadleaf weed control of glyphosate-resistant weeds in field corn.\nThe recently "
        "acquired products are complementary tank-mix partners for a variety of primary "
        "herbicides used in the U.S. agricultural market. They are particularly valuable for "
        "enhancing weed control performance against increasing numbers of troublesome weed "
        "species.\nAllows flexible broadleaf weed control in soybeans and field "
        "corn.\nFor more information on Classic Herbicide, FirstRate Herbicide, "
        "Hornet Herbicide and Python Herbicide or other AMVAC products, "
        "visit www.AMVAC.com.\nTweet"
    )
    assert r["created_at"] == "2020-04-07T11:14:34+00:00"
    assert r["title"] == "AMVAC Releases New Logos For Recently Acquired Herbicides"
