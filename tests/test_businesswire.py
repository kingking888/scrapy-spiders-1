"""Test suit for BusinessWire."""

from agblox.spiders.businesswire import BusinessWireSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return BusinessWireSpider()


@pytest.fixture()
def test_kwargs():
    return {"ticker": "TWTR", "last_url": None}


headers = headers(BusinessWireSpider.host_header)
headers["User-Agent"] = BusinessWireSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.businesswire.com/portal/site/home/news/",
            headers,
            [
                "https://www.businesswire.com/news/home/20210301005502/en/Advent-Technologies-Announces-Official-Launch-of-Joint-Collaboration-With-U.S.-Department-of-Energy-for-Next-Generation-Fuel-Cell-Technology",
                "https://www.businesswire.com/news/home/20210301005659/en/Insights-on-the-Penetration-Testing-Global-Market-to-2027---Featuring-Acunetix-Checkmarx-and-IBM-Among-Others---ResearchAndMarkets.com",
                "https://www.businesswire.com/news/home/20210301005658/en/UK-Regulatory-Announcement-Net-Asset-Value-s",
                "https://www.businesswire.com/news/home/20210301005657/en/UK-Regulatory-Announcement-Net-Asset-Value-s",
                "https://www.businesswire.com/news/home/20210301005656/en/Global-1143-Billion-Iron-and-Steel-Mills-and-Ferroalloy-Markets-2015-2020-2020-2025F-2030F---ResearchAndMarkets.com",
                "https://www.businesswire.com/news/home/20210301005654/en/NPR-Announces-2021-How-I-Built-This-Fellowship-Application",
                "https://www.businesswire.com/news/home/20210301005652/en/Global-Pharmacovigilance-Market-2020-to-2028---Impact-Analysis-of-COVID-19-on-Growth-Opportunities---ResearchAndMarkets.com",
                "https://www.businesswire.com/news/home/20210301005653/en/Everbridge-Announces-Next-Generation-of-Mobile-App-for-Organizations-to-Manage-the-Full-Lifecycle-of-a-Critical-Event-from-a-Device",
                "https://www.businesswire.com/news/home/20210301005041/en/Preventative-Wellness-Startup-Reperio-Health-Nets-6-Million-in-Seed-Funding-to-Expand-Proactive-Health-Monitoring",
                "https://www.businesswire.com/news/home/20210301005650/en/Two-Day-Online-Seminar-Ensuring-Compliance-with-Advertising-and-Promotional-Requirements-for-Drugs-and-Medical-Devices---March-18-19-2021---ResearchAndMarkets.com",
                "https://www.businesswire.com/news/home/20210301005651/fr",
                "https://www.businesswire.com/news/home/20210301005593/en/EMASS-Senior-Softball-League-Opens-Registration-for-2021-Season",
                "https://www.businesswire.com/news/home/20210301005649/en/Domtar-Corporation-Completes-Sale-of-Personal-Care-Business",
                "https://www.businesswire.com/news/home/20210301005010/en/Students-Invited-to-Get-A-Head-Start-on-College-and-Career-Goals-at-Destinations-Career-Academy-of-Colorado",
                "https://www.businesswire.com/news/home/20210301005635/en/UK-Regulatory-Announcement-Block-listing-Interim-Review",
                "https://www.businesswire.com/news/home/20210301005645/en/Global-Renewable-Methanol-Market-2021-2028---Shifting-Trend-Towards-Sustainable-Energy-Sources---ResearchAndMarkets.com",
                "https://www.businesswire.com/news/home/20210301005643/en/Global-Network-Configuration-and-Change-Management-Industry-2020-to-2027---Market-Trajectory-Analytics---ResearchAndMarkets.com",
                "https://www.businesswire.com/news/home/20210301005198/en/SIMON-Welcomes-Brighthouse-Financial-to-Annuities-Platform",
                "https://www.businesswire.com/news/home/20210301005218/en/Evenflo%C2%AE-Gold-Launches-Revolve360%E2%84%A2-a-Turning-Point-in-Car-Seat-Innovation",
                "https://www.businesswire.com/news/home/20210301005640/en/World-Interactive-Kiosk-Market-Size-Share-Trends-Analysis-2021-2028-Focus-on-Customized-Service-Delivery-by-Major-Industry-Players---ResearchAndMarkets.com",
                "https://www.businesswire.com/news/home/20210301005443/en/UK-Regulatory-Announcement-Form-8.3---Applegreen-plc",
                "https://www.businesswire.com/news/home/20210301005447/en/UK-Regulatory-Announcement-Form-8.3---Scapa-Group-plc",
                "https://www.businesswire.com/news/home/20210301005501/en/UK-Regulatory-Announcement-Form-8.3---RSA-Insurance-Group-plc",
                "https://www.businesswire.com/news/home/20210301005529/en/UK-Regulatory-Announcement-Form-8.3---Signature-Aviation-plc",
                "https://www.businesswire.com/news/home/20210301005441/en/UK-Regulatory-Announcement-Form-8.3---AA-plc",
                "https://www.businesswire.com/portal/site/home/template.PAGE/news/?javax.portlet.tpst=ccf123a93466ea4c882a06a9149550fd&javax.portlet.prp_ccf123a93466ea4c882a06a9149550fd_viewID=MY_PORTAL_VIEW&javax.portlet.prp_ccf123a93466ea4c882a06a9149550fd_ndmHsc=v2*A1612011600000*B1614613071176*DgroupByDate*G2*N1000003&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken",
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
            "https://www.businesswire.com/news/home/20210301005645/en/Global-Renewable-Methanol-Market-2021-2028---Shifting-Trend-Towards-Sustainable-Energy-Sources---ResearchAndMarkets.com",
            headers,
        ),
    ],
)
def test_article(spider, response, test_kwargs):
    r = next(spider.parse_article(response=response, **test_kwargs))
    assert (
        r["text"]
        == """DUBLIN--( )--The report has been added to offering.\nGlobal market for renewable methanol, predicts that the industry is likely to witness a CAGR of 3.16% by revenue and 2.08% by volume over the forecasting duration of 2021-2028.\nThere has been a growing inclination towards the adoption of sustainable energy sources, which is one of the major growth-inducing factors for this market. Plus, the rigid governmental rules & regulations and the availability of renewable methanol are contributing to this growth. However, factors like the high costs required for the installation of these sources are hindering this growth process. Despite this, the industry has several opportunities for growth, which includes the usage of renewable methanol as a substitute to heave marine fuels.\nThe market in North America is expected to grow the fastest worldwide, over the forthcoming years. In this market, the US is expected to grow at the fastest rate. The share of renewable energy in generating power is on the rise in the US. The nation is the largest producer of biofuel in the world. Liquid biofuels and electric vehicles (EVs) are the two main technology options in the transport sector.\nMoreover, high-speed trains that use renewable power instead of diesel-based trucks, or city trams for passenger cars, are the other available options for transport. These factors are leading to an enhanced demand for renewable methanol in the country, which is expected to help the market to grow in the years to come.\nThe main contenders in the renewable methanol market include Enerkem, Serenergy A/S, Southern Chemical Corporation, Fraunhofer, Advanced Chemical Technologies, Nordic Green, Carbon Recycling International (CRI), Methanex Corporation, OCI NV, BASF SE, Gujarat Narmada Valley Fertilizers & Chemicals Ltd, Oberon Fuels, Innogy, Atlantic Methanol, and Sodra.\nMethanex Corporation is a Canadian company engaged in producing and supplying methanol to several markets across the globe, such as North America, South America, Europe, and the Asia-Pacific. In New Zealand, the company has three plants, through which it supplies methanol to customers, mainly in the APAC region.\nWhereas, in Trinidad, it has two plants, named Atlas and Titan, through which it supplies methanol to markets worldwide. Methanex's Egypt-based joint venture is situated near the Mediterranean Sea, which primarily supplies the fuel to the domestic market and Europe.\nFurther, the company's Alberta-based plant located in the city of Medicine Hat, supplies methanol to buyers across the North American region. Two of the company's plants in Chile's Punta Arenas, supply methanol to end-users in South America and across the world.\n2.1. Key Insights\n2.1.1. Renewable Methanol Production Using Electricity, Electrolysis of Water, and Co2 Air Capture\n2.1.2. Renewable Methanol from Biogas\n2.1.3. Renewable Methanol as a Fuel for the Shipping Industry\n2.2. Market Definition\n2.3. Porter's Five Forces Analysis\n2.4. Market Attractiveness Index\n2.5. Vendor Scorecard\n2.6. Regulatory Framework\n2.7. Impact of Covid-19 on Renewable Methanol\n2.8. Key Market Strategies\n2.8.1. Partnership, Contract/Agreement, and Collaboration\n2.8.2. Business Expansion\n2.9. Market Drivers\n2.9.1. Shifting Trend Towards Sustainable Energy Sources\n2.9.2. Availability of Renewable Methanol\n2.9.3. Stringent Government Rules and Regulations\n2.10. Market Restraints\n2.10.1. High Installation Cost\n2.10.2. Health Concerns\n2.11. Market Opportunities\n2.11.1. Substitution of Heave Marine Fuels With Renewable Methanol\n3.1. Chemical\n3.2. Transportation\n3.3. Power Generation\n3.4. Others\n4.1. Agricultural Waste\n4.2. Forestry Residue\n4.3. Municipal Solid Waste\n4.4. Co2 Emission\n4.5. Others\n5.1. Formaldehyde\n5.2. Dimethyl Ether (DME, Also Known as Methoxymethane) and Methyl Tert-Butyl Ether (MTBE)\n5.3. Gasoline\n5.4. Solvent\n5.5. Others\n7.1. Advanced Chemical Technologies\n7.2. BASF Se\n7.3. Carbon Recycling International (Cri)\n7.4. Enerkem\n7.5. Fraunhofer\n7.6. Innogy\n7.7. Nordic Green\n7.8. OCI Nv\n7.9. Serenergy A/S\n7.10. Sodra\n7.11. Methanex Corporation\n7.12. Gujarat Narmada Valley Fertilizers & Chemicals Ltd\n7.13. Southern Chemical Corporation\n7.14. Atlantic Methanol\n7.15. Oberon Fuels\nFor more information about this report visit"""
    )
    assert r["created_at"] == "2021-03-01T15:24:00Z"
    assert r["tags"] == ["businesswire", "article", "equity"]
    assert (
        r["title"]
        == "Global Renewable Methanol Market 2021-2028 - Shifting Trend Towards Sustainable Energy Sources - ResearchAndMarkets.com"
    )
