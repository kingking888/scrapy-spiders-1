"""Test suit for AgfaxSpider."""

from agblox.spiders.fisker import FiskerInvestorSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return FiskerInvestorSpider()


headers_dict = headers(FiskerInvestorSpider.host_header)
headers_dict["User-Agent"] = FiskerInvestorSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            FiskerInvestorSpider.url,
            headers_dict,
            [
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-Inc.-to-Participate-in-Upcoming-Barclays-Global-Automotive-Virtual-Conference/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-and-Magna-Achieve-Key-Engineering-and-Purchasing-Milestones/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-to-Ring-the-Opening-Bell-at-the-New-York-Stock-Exchange/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-Inc.-Closes-Business-Combination-Will-Begin-Trading-on-the-NYSE-as-FSR-on-October-30-2020/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-Inc.-to-Establish-European-Headquarters-in-Munich-Ocean-SUV-Program-Advancing-Towards-First-Gateway/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-Inc.-Set-to-Reveal-Production-Ocean-SUV-at-the-Los-Angeles-Auto-Show-May-2021/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-Inc.-and-Viggo-Sign-Agreement-for-Future-Delivery-of-300-Vehicles-to-Support-Next-Generation-Urban-Mobility-Growth/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-Announces-Strategic-Cooperation-With-Magna/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-Inc.-to-Establish-New-Global-Headquarters-in-Los-Angeles/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/John-Finnucan-Appointed-Chief-Accounting-Officer-at-Fisker-Inc/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-Inc.-Appoints-Bill-McDermott-To-Board-Of-Directors/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-Inc.-to-Establish-New-Technology-Center-in-San-Francisco/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Dan-Galves-Appointed-Vice-President-Investor-Relations-at-Fisker-Inc/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-Inc.-Announces-Board-of-Directors/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-Inc.-to-List-on-Nyse-Through-Merger-with-Apollo-Affiliated-Spartan-Energy-Acquisition-Corp/default.aspx",
                "https://investors.fiskerinc.com/news/news-details/2020/Fisker-Commits-to-Global-Leadership-in-Measuring-and-Reporting-on-Environmental-Social-and-Governance-Practices/default.aspx",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://investors.fiskerinc.com/news/news-details/2020/Dan-Galves-Appointed-Vice-President-Investor-Relations-at-Fisker-Inc/default.aspx",
            headers_dict,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["url"]
        == "https://investors.fiskerinc.com/news/news-details/2020/Dan-Galves-Appointed-Vice-President-Investor-Relations-at-Fisker-Inc/default.aspx"
    )
    assert (
        r["text"]
        == "LOS ANGELES , Aug. 31, 2020 /PRNewswire/ -- Fisker Inc. – designer and manufacturer of the world's most emotion-stirring, eco-friendly electric vehicles and advanced mobility solutions – today announced the appointment of Dan Galves as vice president, investor relations, effective Sept. 1 . \"Dan brings a wealth of experience to Fisker Inc. and will be integral to communicating the company's revolutionary business model to the financial markets. As we challenge conventional thinking across every area of the automotive industry, Dan understands our vision and will be part of the management team to help realize it,\" said Henrik Fisker , chairman and CEO of Fisker Inc. Commenting on his appointment at Fisker Inc., Dan said: \"Automotive consumers are increasingly realizing that they can have it all: compelling performance, cutting-edge user experience, environmental sustainability and flexible ownership models. I believe that Fisker has the right business model to provide the product experience that today's (and tomorrow's) consumer will value…and the capability to execute that vision. I'm thrilled to be joining to support the company's exciting path.\" Dan has spent 11 years interacting with industrial and tech-focused investors as a research analyst, with particular expertise in vehicle electrification and automation. He joins from Wolfe Research, where he covered the automotive technology sector and co-led Wolfe's automotive research team (ranked No. 1 by Institutional Investor Magazine in 2019). His analyst career also includes stints at Deutsche Bank and Credit Suisse from 2007-2016. Prior to joining Wolfe Research in August 2018 , Dan was the director of autonomous driving communications at Intel Corp., following their acquisition of Mobileye, where he was the primary point of contact for investors and media as chief communications officer from May 2016 . For investor-related questions, please email Investors@GoDRIVEN360.com – and for media interview inquiries, contact Fisker@GoDRIVEN360.com . About Fisker Inc. California -based Fisker Inc. is revolutionizing the automotive industry by developing the most emotionally desirable and eco-friendly electric vehicles on Earth. Passionately driven by a vision of a clean future for all, the company is on a mission to become the No. 1 e-mobility service provider with the world's most sustainable vehicles. To learn more, visit www.FiskerInc.com – and enjoy exclusive content across Fisker's social media channels: Facebook , Instagram , Twitter , YouTube and LinkedIn . Download the revolutionary new Fisker mobile app from the App Store or Google Play store. SOURCE Fisker Inc. http://www.FiskerInc.com"
    )
    assert r["created_at"] == "2020-08-31T00:00:00+00:00"
    assert r["title"] == "Dan Galves Appointed Vice President, Investor Relations at Fisker Inc."
