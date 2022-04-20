"""Test suit for AgfaxSpider."""

from agblox.spiders.fieldcropnews import FieldCropNewsSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return FieldCropNewsSpider()


headers_dict = headers(FieldCropNewsSpider.host_header)
headers_dict["User-Agent"] = FieldCropNewsSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            FieldCropNewsSpider.url,
            headers_dict,
            [
                "https://fieldcropnews.com/2020/11/2020-dry-edible-bean-seasonal-summary/",
                "https://fieldcropnews.com/2020/11/2020-canola-seasonal-summary/",
                "https://fieldcropnews.com/2020/11/2020-forage-seasonal-summary/",
                "https://fieldcropnews.com/2020/11/cover-crop-based-organic-no-till-soybean-production-in-ontario/",
                "https://fieldcropnews.com/2020/10/understanding-the-impact-and-measures-needed-to-address-bt-resistant-rootworm/",
                "https://fieldcropnews.com/2020/10/2020-ontario-grain-corn-ear-mould-and-deoxynivalenol-don-mycotoxin-survey/",
                "https://fieldcropnews.com/2020/10/non-corn-options-for-livestock-producers-to-manage-bt-resistant-corn-rootworm/",
                "https://fieldcropnews.com/2020/10/mitigation-measures-for-bt-resistant-corn-rootworm/",
                "https://fieldcropnews.com/2020/10/revised-october-2020-canadian-bt-corn-trait-tables-with-events-and-resistance-status/",
                "https://fieldcropnews.com/2020/10/september-2020-forage-report/",
                "https://fieldcropnews.com/2020/09/getting-to-know-your-knolls-part-2-understanding-and-managing-low-ph-knolls/",
                "https://fieldcropnews.com/2020/09/getting-to-know-your-knolls-part-1-understanding-and-managing-high-ph-knolls/",
                "https://fieldcropnews.com/2020/09/unraveling-the-mystery-of-soil-manures-contribution/",
                "https://fieldcropnews.com/2020/09/frost-injury-in-sorghum-species/",
                "https://fieldcropnews.com/2020/09/managing-jointing-and-non-jointing-grasses/",
                "https://fieldcropnews.com/page/2/",
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
            "https://fieldcropnews.com/page/79/",
            headers_dict,
            [
                "https://fieldcropnews.com/2009/06/bean-leaf-beetle-adults-active-and-some-cereal-leaf-beetle-too/",
                "https://fieldcropnews.com/2009/06/soybean-aphids-found-near-london-e-ontario-and-s-quebec/",
                "https://fieldcropnews.com/2009/06/soybean-aphids-on-soys-in-michigan-now-too/",
                "https://fieldcropnews.com/2009/06/soybean-aphids-on-soybeans-in-iowa/",
                "https://fieldcropnews.com/2009/06/armyworm-spotted-in-essex-county/",
                "https://fieldcropnews.com/2009/05/cutworm-cutting/",
                "https://fieldcropnews.com/2009/05/not-much-happening-yet/",
                "https://fieldcropnews.com/2009/05/alfalfa-weevil-and-armyworm/",
                "https://fieldcropnews.com/2009/05/handy-search-site-for-product-labels/",
                "https://fieldcropnews.com/2009/05/things-to-be-looking-for/",
                "https://fieldcropnews.com/2009/05/hello-and-welcome/",
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
            "https://fieldcropnews.com/2009/05/alfalfa-weevil-and-armyworm/",
            headers_dict,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["url"] == "https://fieldcropnews.com/2009/05/alfalfa-weevil-and-armyworm/"
    assert r["text"] == (
        "Alfalfa Weevil – We are starting to see a lot more alfalfa weevil larvae in the fields "
        "we are scouting. Many fields in southwestern Ontario are ready or close to being ready "
        "to be cut. I know you are busy trying to get everything planted finally, but I encourage "
        "guys to get out and cut the hay (if field is ready) to reduce the risk of injury from "
        "alfalfa weevil larvae. If fields are not fit or ready to cut, you’ll need to scout and "
        "determine if the larvae are reaching threshold. Again, cutting is the first choice for "
        "management if possible, if it is not, then spray at threshold.\nArmyworm – It was "
        "around this time last year we started to see armyworm larvae appear in the fields. We "
        "did catch a few moths in April and with all of the storm fronts that continued to come "
        "our way, there could have been more blown into Ontario. Scout both the borders and "
        "randomly within wheat fields. And soon to emerge corn fields are at risk too. There were "
        "so many fields with weeds that didn’t get sprayed until now that were ideal for the "
        "moths to lay their eggs on. Larvae could have survived on those weeds until the crop "
        "pops up out of the ground. And they will be bigger (and harder to kill) when they do "
        "move over to the crop.\nLet me know if you find any so we can get the word "
        "out!\nTracey Baute\n2009-05-21"
    )
    assert r["created_at"] == "2009-05-21T00:00:00+00:00"
    assert r["title"] == "Alfalfa Weevil and Armyworm"
