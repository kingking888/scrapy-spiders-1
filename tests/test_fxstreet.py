"""Test suit for FXStreet."""
from agblox.spiders.fxstreet import FXStreetSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return FXStreetSpider()


_headers = headers(FXStreetSpider.host_header)
_headers["User-Agent"] = FXStreetSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.fxstreet.com/news/australia-queensland-state-premier-greater-brisbane-to-go-into-three-day-covid-lockdown-reuters-202101072222",
            _headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["url"]
        == "https://www.fxstreet.com/news/australia-queensland-state-premier-greater-brisbane-to-go-into-three-day-covid-lockdown-reuters-202101072222"
    )
    assert r["text"] == (
        "Early Friday morning in Asia, Queensland’s State Premier Annastacia Palaszczuk announced "
        "a three-day activity restriction in Greater Brisbane, per Reuters. The news cites "
        "Thursday’s founding of the UK coronavirus strain as the key reason for the latest "
        'lockdown. The restrictions also make mask-wearing compulsory.\n"We will be mandating '
        'masks in those areas if you are leaving home," said Ms. Palaszczuk.\nThe policymaker '
        'also mentioned, "So, if you are leaving home, you are leaving your place of residence, '
        "from 6:00 pm Friday to 6:00 pm Monday and you will living in those council areas, again, "
        "let me say them - Brisbane, Logan, Ipswich, Moreton and Redlands - you must wear a "
        'mask."\nState Premier Palaszczuk also said that If we do not do this now, it could end '
        "up being a 30-day lockdown.\nOn the positive side, Victoria marks zero locally "
        "acquired cases of the coronavirus (COVID-19).\nFX implications\nAUD/USD cools down "
        "to 0.7760, from 0.7773, while following the news . However, optimism concerning the US "
        "stimulus keeps the bulls hopeful.\nRead: AUD/USD eyes 0.7800 as bulls fight amid "
        "upbeat market mood"
    )
    assert r["created_at"] == "2021-01-07T22:22:51Z"
    assert (
        r["title"]
        == "Australia Queensland State Premier: Greater Brisbane to go into three-day covid lockdown - Reuters"
    )
