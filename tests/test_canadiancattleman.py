"""Test suit for PurdueSpider."""

from agblox.spiders.canadiancattleman import CanadiancattlemanSpider
from agblox.spiders.helpers import headers
import pytest


@pytest.fixture()
def spider():
    return CanadiancattlemanSpider()


headers = headers(CanadiancattlemanSpider.host_header)
headers["User-Agent"] = CanadiancattlemanSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            CanadiancattlemanSpider.url,
            headers,
            [
                "https://www.canadiancattlemen.ca/cca-reports/cca-reports-leveraging-public-interest-in-agriculture/",
                "https://www.canadiancattlemen.ca/news/accolades-for-bovine-veterinarian-practitioner/",
                "https://www.canadiancattlemen.ca/features/barbados-aiming-for-self-sufficiency-in-food-production/",
                "https://www.canadiancattlemen.ca/markets/sustainability-efforts-in-the-beef-industry-growing/",
                "https://www.canadiancattlemen.ca/news/research-network-to-allocate-15-million-in-first-open-call-for-proposals/",
                "https://www.canadiancattlemen.ca/news/condolences-to-the-ballard-family/",
                "https://www.canadiancattlemen.ca/news/manitoba-youth-beef-roundup-holds-cattle-photography-workshop-scholarships-awarded/",
                "https://www.canadiancattlemen.ca/news/cody-sibbald-legacy-classic-cancelled-for-2020/",
                "https://www.canadiancattlemen.ca/cca-reports/cca-reports-trade-access-livestock-price-insurance-and-agristability/",
                "https://www.canadiancattlemen.ca/news/canadian-junior-shorthorn-association-virtual-show-results/",
                "https://www.canadiancattlemen.ca/events/moved-online-vision-2020-canadian-forage-and-grassland-association-conference/",
                "https://www.canadiancattlemen.ca/events/advancing-women-in-agriculture-awc-east-2020/",
                "https://www.canadiancattlemen.ca/events/cultivating-trust-farm-and-food-care-saskatchewan-online-conference/",
                "https://www.canadiancattlemen.ca/news/page/2/",
            ],
        ),
    ],
)
def test_first_page(spider, response, expected):
    r = [e.url for e in spider.parse(response)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            "https://www.canadiancattlemen.ca/news/page/81/",
            headers,
            [
                "https://www.canadiancattlemen.ca/news/does-anyone-use-lidocaine-when-dehorning-their-calves/",
                "https://www.canadiancattlemen.ca/news/changing-the-rules-about-food/",
                "https://www.canadiancattlemen.ca/news/the-value-of-manure/",
                "https://www.canadiancattlemen.ca/news/letters-for-jan-19-2009/",
                "https://www.canadiancattlemen.ca/news/suggestions-are-always-welcome-my-phone-number-is-4033251695-email-debwilson-fbcpublishingcom/",
                "https://www.canadiancattlemen.ca/news/the-time-for-help-is-now/",
                "https://www.canadiancattlemen.ca/news/calving-tips-tales-for-jan-19-2009/",
                "https://www.canadiancattlemen.ca/news/letters-for-jan-5-2009/",
                "https://www.canadiancattlemen.ca/news/newsmakers-for-jan-5-2009/",
                "https://www.canadiancattlemen.ca/events/moved-online-ontario-agricultural-conference/",
                "https://www.canadiancattlemen.ca/events/cancelled-manitoba-ag-days/",
                "https://www.canadiancattlemen.ca/events/saskatchewan-beef-industry-conference/",
                "https://www.canadiancattlemen.ca/news/page/82/",
            ],
        ),
    ],
)
def test_last_page(spider, response, expected):
    spider.page = 81
    r = [e.url for e in spider.parse(response)]
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://www.canadiancattlemen.ca/cca-reports/cca-reports-leveraging-public-interest-in-agriculture/",
            headers,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["text"] == (
        "The past year has been a challenging one for our industry as we cope with the impacts from the COVID-19 pandemic. It is easy to only look at the negative outcomes and not see a silver lining, but there are definitely a couple of positives we need to capitalize on as an industry. Over the past seven months, the Canadian agricultural industry has seen Canadians become more aware of where their food comes from and they are asking more questions about food production in Canada. We have a meaningful and significant opportunity to share our industry’s story and raise awareness of the sustainable production practices we embrace on Canadian beef farms and ranches. CCA reports: Trade access, livestock price insurance and AgriStability CCA reports: Supporting young producers through COVID and beyond CCA Reports: Linking conservation and cattle ADVERTISEMENT We have worked hard to share this message in Ottawa with policy-makers. Earlier this fall, the new parliamentary session opened with the speech from the throne. This speech provided insights into the key priorities of the federal government during these uncertain times. We were keen to see the Government of Canada acknowledge the role our farmers and ranchers across Canada play in the fight against climate change. Most importantly is how producers will continue to focus on these important discussions about the benefits of beef production to our environment and our economic recovery post COVID-19. Through the National Beef Strategy, we continually commit to enhancements to the productivity and competitiveness of the Canadian beef industry, as well as bolstering beef demand. We strive to communicate the efforts undertaken by beef producers to care for their land, their animals and the environment, which is critical to building trust with Canadians. ADVERTISEMENT To build upon the five-year goals outlined in the 2020-2024 National Beef Strategy, our industry identified a suite of ambitious 10-year goals for all national beef organizations to aim for together. The aim is for these goals to result in significant innovation within our industry and to solidify our role as a bona fide solution provider to climate change. The first of three goal topics were released at the Canadian Roundtable of Sustainable Beef’s (CRSB) annual general meeting in September. They focus on greenhouse gas and carbon sequestration, animal health and welfare, and land use and biodiversity. Future goal setting will focus on water, beef quality and food safety, human health and safety, and technology, to be completed in 2021. Through a series of webinars hosted by CRSB this fall, input will be gathered to develop robust, action-oriented goals for these remaining topic areas. Be sure to look for updates on the consultation process and release of the goals associated with these important topics coming in 2021. ADVERTISEMENT The CCA will leverage these goals working with all levels of government to strengthen support for beef production across Canada and expand our outreach and policy efforts. The target is to enhance opportunities to partner on policy, especially environmental policy solutions we can crystalize with the federal government. Of course, we aim to counter the negative public misunderstandings related to these issues. Currently, we are engaging the federal government on a number of key files with an environmental focus and hope the comments included in the speech from the throne will result in meaningful consultation and community-led and -managed engagement to achieve positive outcomes. Over the past number of years, CCA has keyed in on discussions with parliamentarians, senators, and government officials concerning Bill C-68, the Fisheries Act. CCA actively communicated our concerns with the “deeming habitat” provision of the act and were able to influence its removal during the Senate review process. The act received royal assent in June 2019 prior to the regulations being developed. The Department of Fisheries and Oceans (DFO) pledged to consult with stakeholders on the development of standards, codes of practice and prescribed works regulations. DFO has reached out to the agricultural sector informally regarding the development of six interim codes of practice, and we have provided initial feedback on these codes before they are to be finalized this fall. CCA does have concerns regarding the Interim Code of Practice for Beaver Dam Removal, which states that beaver dams are only to be removed by hand with no use of heavy equipment. CCA has provided comments to DFO on this code to offer a different approach allowing for the use of heavy equipment to remove beaver dams, while minimizing potential sediment downstream or in the impoundment. CCA has also requested further clarification on the text included in this code concerning sediment control plans and measures, which is somewhat confusing and contradictory. CCA is also engaging with DFO for clarity on the development of recovery strategies for specific aquatic species including bull trout, chinook and coho salmon, and others, as it is unclear how critical habitat is determined and apparently results in significant restrictions being applied to landowners. CCA aims to engage in meaningful consultation around these recovery strategies and will include agricultural stakeholders. Last, recognizing the role that Canadian beef producers play in managing our grasslands, CCA broadly supports the idea of beef producers being reimbursed for ecological goods and services in a flexible manner that meets the end goals of their operation. CCA encourages the development of a national framework for ecosystem services delivered regionally with buyers and sellers involved. We will continue to deliver our strong environmental story in Ottawa and advocate for opportunities for continued input by stakeholders in our industry for meaningful outcomes that work for beef producers in regions across Canada."
    )
    assert r["created_at"] == "2020-11-13T00:00:00+00:00"
    assert r["tags"] == spider.tags
    assert r["title"] == "CCA reports: Leveraging public interest in agriculture"
