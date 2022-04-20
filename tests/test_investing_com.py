"""Test suit for InvestingSpider."""

from agblox.spiders.helpers import headers
from agblox.spiders.investing import InvestingSpider
import pytest


@pytest.fixture()
def spider():
    return InvestingSpider()


headers_dict = headers(InvestingSpider.host_header)
headers_dict["User-Agent"] = InvestingSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            InvestingSpider.url,
            headers_dict,
            [
                "https://www.investing.com/news/stock-market-news/gamestop-slides-silver-spree-stalls-as-retail-traders-run-out-of-road-2406154",
                "https://www.investing.com/news/stock-market-news/pfizer-exxon-mobil-and-ups-rise-premarket-gamestop-falls-2406445",
                "https://www.investing.com/news/economy/squeeze-eases-dollar-rises-amazon-alphabet-earnings--whats-up-in-markets-2406270",
                "https://www.investing.com/analysis/1-stock-to-buy-1-to-dump-when-markets-open-penn-national-gaming-apple-200557620",
                "https://www.investing.com/analysis/3-stocks-to-watch-in-the-coming-week-gamestop-amazon-alphabet-200557612",
                "https://www.investing.com/analysis/gamestop-frenzy-signals-markets-are-in-bubble-territory-200557677",
                "https://www.investing.com/news/forex-news/dollar-weakens-stimulus-progression-boosts-risk-sentiment-2406047",
                "https://www.investing.com/news/forex-news/dollar-down-but-near-sevenweek-highs-after-euro-selloff-2405975",
                "https://www.investing.com/news/forex-news/dollar-hovers-near-sevenweek-high-after-boost-from-euro-selloff-2405951",
                "https://www.investing.com/news/forex-news/pound-drifts-lower-ahead-of-boe-decision-negative-rate-report-eyed-2405579",
                "https://www.investing.com/news/forex-news/dollar-edges-higher-caution-reigns-as-week-starts-2404742",
                "https://www.investing.com/news/forex-news/dollar-down-concerns-over-hedge-fund-and-retail-investor-battle-remain-2404650",
                "https://www.investing.com/news/forex-news/dollar-supported-by-haven-demand-after-retail-frenzy-bruises-risk-sentiment-2404618",
                "https://www.investing.com/news/forex-news/dollar-gains-risk-sentiment-hit-by-equity-turmoil-2402977",
                "https://www.investing.com/news/forex-news/cargill-deutsche-bank-among-firms-taiwan-accuses-of-fx-speculation-2402895",
                "https://www.investing.com/news/forex-news/dollar-makes-small-gains-with-higher-us-treasury-yields-2402853",
                "https://www.investing.com/news/forex-news/safehaven-dollar-softens-as-risk-sentiment-recovers-2402785",
                "https://www.investing.com/news/forex-news/pounds-shrugs-off-warning-of-excessive-optimism-to-hit-more-multiyear-high-2402430",
                "https://www.investing.com/news/forex-news/dollar-in-demand-stocks-selloff-prompts-risk-aversion-2401402",
                "https://www.investing.com/news/forex-news/dollar-rises-as-stock-slump-rattles-investor-confidence-2401272",
                "https://www.investing.com/news/stock-market-news/gamestop-slides-silver-spree-stalls-as-retail-traders-run-out-of-road-2406154",
                "https://www.investing.com/news/stock-market-news/pfizer-exxon-mobil-and-ups-rise-premarket-gamestop-falls-2406445",
                "https://www.investing.com/news/economy/squeeze-eases-dollar-rises-amazon-alphabet-earnings--whats-up-in-markets-2406270",
                "https://www.investing.com/news/stock-market-news/pfizer-sees-about-15-billion-in-2021-sales-from-covid19-vaccine-2406300",
                "https://www.investing.com/news/coronavirus/us-house-democrats-ready-first-stop-toward-19-trillion-covid19-relief-bill-2406535",
                "https://www.investing.com/analysis/1-stock-to-buy-1-to-dump-when-markets-open-penn-national-gaming-apple-200557620",
                "https://www.investing.com/analysis/3-stocks-to-watch-in-the-coming-week-gamestop-amazon-alphabet-200557612",
                "https://www.investing.com/analysis/gamestop-frenzy-signals-markets-are-in-bubble-territory-200557677",
                "https://www.investing.com/analysis/opening-bell-vaccine-progress-drives-markets-higher-as-retail-revolt-eases-200557866",
                "https://www.investing.com/analysis/week-ahead-stock-speculation-vaccines-covid-variants-to-pressure-markets-200557618",
                "https://www.investing.com/news/forex-news/2",
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
            "https://www.investing.com/news/forex-news/4321",
            headers_dict,
            [
                "https://www.investing.com/news/stock-market-news/gamestop-slides-silver-spree-stalls-as-retail-traders-run-out-of-road-2406154",
                "https://www.investing.com/news/stock-market-news/pfizer-exxon-mobil-and-ups-rise-premarket-gamestop-falls-2406445",
                "https://www.investing.com/news/economy/squeeze-eases-dollar-rises-amazon-alphabet-earnings--whats-up-in-markets-2406270",
                "https://www.investing.com/analysis/1-stock-to-buy-1-to-dump-when-markets-open-penn-national-gaming-apple-200557620",
                "https://www.investing.com/analysis/3-stocks-to-watch-in-the-coming-week-gamestop-amazon-alphabet-200557612",
                "https://www.investing.com/analysis/gamestop-frenzy-signals-markets-are-in-bubble-territory-200557677",
                "https://www.investing.com/news/forex-news/global-markets-credit-crisis-fears-spark-global-stock-rout-715",
                "https://www.investing.com/news/forex-news/global-markets-stocks-worldwide,-oil-fall-as-crisis-fears-widen-713",
                "https://www.investing.com/news/forex-news/global-markets-global-stocks,-oil-fall-as-crisis-fears-widen-709",
                "https://www.investing.com/news/forex-news/global-markets-stocks-plunge,-yen-leaps-as-crisis-escalates-700",
                "https://www.investing.com/news/forex-news/forex-euro-sinks,-yen-soars-as-global-bank-fears-deepen-697",
                "https://www.investing.com/news/forex-news/global-markets-u.s.-bailout-plan-passes,-investors-take-profits-686",
                "https://www.investing.com/news/forex-news/global-markets-stocks-rally-on-wells-wachovia-deal,-dollar-gains-682",
                "https://www.investing.com/news/forex-news/global-markets-stocks-hold-up-after-wells-wachovia-deal-673",
                "https://www.investing.com/news/forex-news/forex-dollar-poised-for-biggest-weekly-gain-in-16-years-671",
                "https://www.investing.com/news/forex-news/nikkei-down-1.4-pct-on-economy-fears,-autos-drop-669",
                "https://www.investing.com/news/forex-news/global-markets-u.s.-economic-worries-drive-down-stocks,-oil-662",
                "https://www.investing.com/news/forex-news/global-markets-global-stocks,-oil-slide-on-economic-stress-signs-657",
                "https://www.investing.com/news/forex-news/forex--dollar-steadies-at-fourmonths-high-treasury-yield-tops-3-1440180",
                "https://www.investing.com/news/forex-news/forex--pound-rises-despite-brexit-crisis-yen-gains-1691023",
                "https://www.investing.com/news/stock-market-news/gamestop-slides-silver-spree-stalls-as-retail-traders-run-out-of-road-2406154",
                "https://www.investing.com/news/stock-market-news/pfizer-exxon-mobil-and-ups-rise-premarket-gamestop-falls-2406445",
                "https://www.investing.com/news/economy/squeeze-eases-dollar-rises-amazon-alphabet-earnings--whats-up-in-markets-2406270",
                "https://www.investing.com/news/stock-market-news/pfizer-sees-about-15-billion-in-2021-sales-from-covid19-vaccine-2406300",
                "https://www.investing.com/news/coronavirus/us-house-democrats-ready-first-stop-toward-19-trillion-covid19-relief-bill-2406535",
                "https://www.investing.com/analysis/1-stock-to-buy-1-to-dump-when-markets-open-penn-national-gaming-apple-200557620",
                "https://www.investing.com/analysis/3-stocks-to-watch-in-the-coming-week-gamestop-amazon-alphabet-200557612",
                "https://www.investing.com/analysis/gamestop-frenzy-signals-markets-are-in-bubble-territory-200557677",
                "https://www.investing.com/analysis/opening-bell-vaccine-progress-drives-markets-higher-as-retail-revolt-eases-200557866",
                "https://www.investing.com/analysis/week-ahead-stock-speculation-vaccines-covid-variants-to-pressure-markets-200557618",
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
            "https://www.investing.com/news/coronavirus/jjs-covid19-vaccine-66-effective-in-large-global-trial-2403317",
            headers_dict,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert (
        r["url"]
        == "https://www.investing.com/news/coronavirus/jjs-covid19-vaccine-66-effective-in-large-global-trial-2403317"
    )
    assert r["text"] == (
        "3/3 © Reuters. FILE PHOTO: Vial and sryinge are seen in front of displayed "
        "Johnson&Johnson logo in this illustration taken 2/3 By Julie Steenhuysen "
        "(Reuters) - Johnson & Johnson (NYSE: JNJ ) said on Friday that its "
        "single-dose vaccine was 66% effective in preventing COVID-19 in a large "
        "global trial against multiple variants, giving health officials another "
        "weapon to tackle the pandemic. In the trial of nearly 44,000 volunteers, the "
        "level of protection against moderate and severe COVID-19 varied from 72% in "
        "the United States, to 66% in Latin America and just 57% in South Africa, "
        "from where a worrying variant has spread. The data showed that the vaccine's "
        "effect on the South Africa variant was diminished compared to the unaltered "
        "virus, but infectious disease and public health experts said it can still "
        "help contain the virus spread and prevent deaths. Midstage trial data from "
        "Novavax (NASDAQ: NVAX ) on Thursday also documented lower effectiveness in "
        "South Africa. Rival shots from Pfizer/BioNTech and Moderna (NASDAQ: MRNA ) "
        "were both around 95% effective in preventing symptomatic illness in pivotal "
        "trials when given in two doses. Those trials were conducted mainly in the "
        "United States and before the emergence of new variants. These mean that the "
        "world is racing against time and with limited supplies to vaccinate as many "
        "people as possible, and quickly, to prevent virus surges. COVID-19 is rising "
        "in 37 countries and infections have surpassed 101 million globally. Top U.S. "
        "infectious disease specialist Anthony Fauci said the world needs to "
        "vaccinate quickly to try to get ahead of these changes in the virus. \"It's "
        "really a wake up call for us to be nimble and to be able to adjust as this "
        "virus will continue for certain to evolve,\" Fauci said. J&J's main goal was "
        "the prevention of moderate to severe COVID-19, and the vaccine was 85% "
        "effective in stopping severe disease and preventing hospitalization across "
        "all geographies and against multiple variants 28 days after immunization. "
        'That "will potentially protect hundreds of millions of people from serious '
        "and fatal outcomes of COVID-19,\" Paul Stoffels, J&J's chief scientific "
        "officer, said. J&J shares were down 4% at $162.7 at 1700 GMT, with some Wall "
        "Street analysts saying its vaccine's effectiveness was below those of "
        "rivals. Moderna's stock gained 8% to $172.80. SEEKING APPROVAL J&J plans to "
        "seek emergency use authorization from the U.S. Food and Drug Administration "
        "next week and will soon follow up with the European Union and the rest of "
        "the world. It has said it plans to deliver 1 billion doses of the vaccine, "
        "which it will make in the United States, Europe, South Africa and India, in "
        "2021. Public health officials are counting on it to increase much-needed "
        "supply and simplify immunization in the United States, which has a deal to "
        "buy 100 million doses of J&J's vaccine and an option for an additional 200 "
        "million. J&J said the vaccine would be ready immediately upon emergency "
        'approval, but Stoffels declined to say how many doses. "The key is not only '
        "overall efficacy but specifically efficacy against severe disease, "
        'hospitalization, and death," said Walid Gellad, a health policy associate '
        "professor at the University of Pittsburgh. J&J's vaccine uses a common cold "
        "virus to introduce coronavirus proteins into cells and trigger an immune "
        "response, whereas the Pfizer/BioNTech and Moderna vaccines employ a new "
        "technology called messenger RNA. Unlike these vaccines, J&J's does not "
        "require a second shot weeks after the first or need to be kept frozen, "
        "making it a strong candidate for use in parts of the world where "
        'transportation and cold storage present problems. "Most countries are still '
        "desperate to get their hands on doses, regardless of whether or not the "
        "vaccine is considered highly effective. Moderately effective will do just "
        'fine for now," Michael Breen, Director of Infectious Diseases and '
        "Ophthalmology at research firm GlobalData, said. 'OVERWHELMED' Several "
        "studies have emerged this month showing that a South African variant has "
        "mutated in areas of the virus that are key targets of vaccines, reducing "
        'their efficacy. "What we are learning is there is different efficacy in '
        'different parts of the world," Stoffels told Reuters. In a sub-study of '
        "6,000 volunteers in South Africa, Stoffels said, the J&J vaccine was 89% "
        "effective at preventing severe disease. In the South Africa portion of the "
        'trial, 95% of cases were infections with the South African variant. "I am '
        "overwhelmed by the fact that this vaccine protected against severe disease "
        'even in South Africa," said Glenda Gray, the joint lead investigator of the '
        "South African vaccine trial. In the J&J trial, which was conducted in eight "
        "countries, 44% of participants were from the United States, 41% from Central "
        "and South America and 15% from South Africa. Just over a third of the "
        "volunteers were over 60."
    )
    assert r["created_at"] == "2021-01-29T00:00:00+00:00"
    assert r["title"] == "J&J vaccine adds to COVID-19 armoury, includes South African variant"
