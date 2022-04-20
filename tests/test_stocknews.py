"""Test suit for StockNews."""

from agblox.spiders.helpers import headers
from agblox.spiders.stocknews import StockNewsSpider
import pytest


@pytest.fixture()
def spider():
    return StockNewsSpider()


@pytest.fixture()
def last_page_spider():
    s = StockNewsSpider()
    s.skip_most_popular = False
    return s


headers_dict = headers(StockNewsSpider.name)
headers_dict["User-Agent"] = StockNewsSpider.user_agent


@pytest.mark.parametrize(
    ["url", "headers", "expected"],
    [
        (
            StockNewsSpider.url,
            headers_dict,
            [
                "https://stocknews.com/news/spy-inx-dia-iwm-qqq-is-this-another-stock-market-bubble/",
                "https://stocknews.com/news/fan-tan-aces-ylco-4-renewable-energy-etfs-to-thrive-under-biden/",
                "https://stocknews.com/news/nio-gp-better-buy-nio-vs-greenpower-motor/",
                "https://stocknews.com/news/hele-tsla-the-stock-of-the-week-is/",
                "https://stocknews.com/news/rpay-uctt-idex-3-small-cap-tech-stocks-to-own-in-2021-repay-ultra/",
                "https://stocknews.com/news/khc-ally-2-value-stocks-rated-strong-buy-kraft-heinz-and-ally/",
                "https://stocknews.com/news/unp-cni-csx-nsc-its-full-steam-ahead-in-2021-for-these-4-railroad/",
                "https://stocknews.com/news/nflx-should-you-buy-netflix-stock-before-it-releases-earnings-next/",
                "https://stocknews.com/news/pbw-fxl-xlb-3-etfs-to-buy-now-to-capitalize-on-for-the/",
                "https://stocknews.com/news/jmia-is-jumia-a-stock-to-avoid-or-buy-on-the/",
                "https://stocknews.com/news/jnj-johnson-johnson-a-top-notch-healthcare-stock-to-buy-and/",
                "https://stocknews.com/news/wow-should-investors-tune-into-wideopenwest/",
                "https://stocknews.com/news/lb-el-gps-tif-is-l-brands-stock-a-good-buy/",
                "https://stocknews.com/news/dkng-docu-2-high-growth-tech-stocks-to-buy-the-dips/",
                "https://stocknews.com/news/plug-why-is-plug-power-skyrocketing/",
                "https://stocknews.com/news/nvda-qcom-nvidia-vs-qualcomm-which-5g-stock-is-a-better-buy/",
                "https://stocknews.com/news/sh-psq-dog-rwm-think-the-market-is-due-for-a-pullback-buy-these/",
                "https://stocknews.com/news/mj-msos-yolo-thcx-4-cannabis-etfs-to-buy-before-biden-takes-office/",
                "https://stocknews.com/news/tsla-nasdaq-the-best-way-to-get-rich-investing-in-tesla/",
                "https://stocknews.com/news/nbev-should-newage-inc-be-in-your-portfolio/",
                "https://stocknews.com/news/fmc-kar-rvlv-3-must-own-growth-stocks-for-a-bull-market-in-2021/",
                "https://stocknews.com/news/mos-why-mosaic-stock-can-outperform-in-2021/",
                "https://stocknews.com/news/nke-sbux-tgt-tjx-cmg-5-top-rated-consumer-discretionary-stocks-for-2021/",
                "https://stocknews.com/news/gld-gdx-kl-auy-agi-3-gold-miners-to-buy-on-dips-yamana-gold-kirkland/",
                "https://stocknews.com/news/tsla-beem-tesla-vs-beam-global-which-electric-vehicle-charging-stock-is/",
                "https://stocknews.com/top-stories/?pg=2",
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
            "https://stocknews.com/top-stories/?pg=111",
            headers_dict,
            [
                "https://stocknews.com/news/cgc-canopy-growth-reduces-acreage-holdings-acquisition-price/",
                "https://stocknews.com/news/alxn-chart-of-the-day-alexion-pharmaceuticals-alxn/",
                "https://stocknews.com/news/amt-eqix-dlr-wpc-4-reits-to-consider-amidst-economic-uncertainty/",
                "https://stocknews.com/news/race-bki-five-lpsn-race-four-upgraded-stocks-zooming-higher/",
                "https://stocknews.com/news/fds-ally-nov-acn-nbl-top-5-large-cap-dividend-stocks-for-june-25-2020/",
                "https://stocknews.com/news/gt-momo-kss-dont-buy-these-3-stocks/",
                "https://stocknews.com/news/mkc-acn-fds-3-earnings-surprises-ready-to-surge-this-summer/",
                "https://stocknews.com/news/ccl-aal-3-travel-stocks-to-avoid/",
                "https://stocknews.com/news/tpx-cspr-3-mattress-stocks-that-could-bounce-to-new-highs/",
                "https://stocknews.com/news/spy-qqq-how-to-hedge-this-stock-market-rebound/",
                "https://stocknews.com/news/shak-wen-jack-3-fast-food-stocks-primed-for-post-shutdown-profits/",
                "https://stocknews.com/top-stories/?pg=112",
            ],
        ),
    ],
)
def test_last_page(last_page_spider, response, expected):
    r = [e.url for e in last_page_spider.parse(response)]
    assert len(r) == len(expected)
    assert r == expected


@pytest.mark.parametrize(
    ["url", "headers"],
    [
        (
            "https://stocknews.com/news/nio-gp-better-buy-nio-vs-greenpower-motor/",
            headers_dict,
        ),
    ],
)
def test_article(spider, response):
    r = next(spider.parse_article(response))
    assert r["url"] == "https://stocknews.com/news/nio-gp-better-buy-nio-vs-greenpower-motor/"
    assert (
        r["text"]
        == "NIO – NIO (NIO) and GreenPower Motor (GP) were the two electric vehicle manufacturers "
        "which saw the highest gains in 2020. Which stock is a better buy for 2021?. Jan 13, "
        "2021 Join thousands of investors who get the latest news, insights and top rated "
        "picks from StockNews.com! Electric vehicle (EV) stocks continue to excite investors, "
        "as the transition towards clean energy gains pace. In just the first 7 days of "
        "trading in 2021, the KraneShares Electric Vehicles & Future Mobility Index ETF ( KARS "
        ") is up over 12%. Driven by technological advancements, as well as government "
        "subsidies and economies of scale, growth in the EV industry will remain strong for "
        "quite some time. According to a Goldman Sach, EVs will account for 18% of global new "
        "light vehicle sales in 2030 and then jump to 29% in 2035. With this in mind, "
        "I decided to take a look at and compare the two EV stocks that had the strongest "
        "gains in 2020: NIO ( NIO ) , which gained more than 1,100%, and GreenPower Motor ( GP "
        ") , which gained more than 1,800%. 9 Simple Strategies to GROW Your Portfolio NIO is "
        "one of the largest EV companies There are several things going right for NIO. It is "
        "one of the largest EV players in China, which is the world’s largest market of "
        "battery-powered automobiles. The rise in the purchasing power of the country’s middle "
        "class coupled with supportive government policies will continue to drive demand for "
        "NIO and peers over the long-term. However, the rise in the adoption of EVs in China "
        "meant the government reduced subsidies by 20% in 2021. It remains to be seen if this "
        "will impact demand for NIO and other EV manufacturers this year. In December 2020, "
        "NIO delivered 7,007 vehicles, a rise of 121% year-over-year. For 2020, the company’s "
        "deliveries stood at 43,728, up 113% year-over-year. NIO recently raised $2.65 billion "
        "in an equity offering to support its growth initiatives. The company also announced "
        "plans to issue convertible debt and raise $1.3 billion to strengthen its balance "
        "sheet as well as improve liquidity. NIO continues to expand its product portfolio and "
        "also showcased the ET7 during its annual NIO Day program. The ET7 is a luxury sedan "
        "with a battery range of 620 miles and the vehicle is expected to be priced at $69,"
        "100. NIO is valued at a market cap of $97 billion indicating a forward price to 2021 "
        "sales multiple of almost 20x. However, its strong growth rates might support its "
        "steep valuation especially if the company is able to consistently beat Wall Street "
        "estimates going forward. GreenPower Motors is a Canadian-based EV GreenPower Motors "
        "is not as established a name as Tesla or NIO. GP, in fact, is part of the high-growth "
        "electric vehicle segment in the medium and heavy-duty commercial vertical. The "
        "company has an asset-light business model which allows it to maintain solid profit "
        "margins due to lower manufacturing costs. For example, the company has spent just $2 "
        "million in research and development costs since 2017, as it uses off-the-shelf "
        "components that enable it to lower costs significantly. GreenPower sells vehicles in "
        "partnership with Creative Bus Sales which is the largest network of bus retailers in "
        "the country. This business model will help GreenPower to increase profit margins at a "
        "higher rate compared to its revenue, indicating it will benefit from operating "
        "leverage. GreenPower expects the medium and heavy-duty commercial EV market to hit "
        "50,000 in annual vehicle deliveries by 2025. GreenPower has a forward price to fiscal "
        "2022 sales multiple of 15. While the company is still posting an adjusted loss, "
        "analysts expect the bottom-line to improve from a loss per share of $0.34 in fiscal "
        "2020 to earnings of $0.22 in fiscal 2022. The verdict GreenPower is not only trading "
        "at a lower valuation compared to NIO, it is also improving profitability at a fast "
        "clip compared to its Chinese counterpart. However, GreenPower is still a small-cap "
        "company and this investment carries a higher risk-reward ratio compared with NIO. "
        "Therefore, I believe NIO is a better investment right now. Although the stock is "
        "trading at a premium, its leadership position in China and its rapidly expanding "
        "market makes it a better bet than GP right now. Want More Great Investing Ideas? 9 "
        "“MUST OWN” Growth Stocks for 2021 5 WINNING Stocks Chart Patterns 7 Best ETFs for the "
        "NEXT Bull Market NIO shares were trading at $63.61 per share on Wednesday morning, "
        "up $1.57 (+2.53%). Year-to-date, NIO has gained 30.51%, versus a 1.31% rise in the "
        "benchmark S&P 500 index during the same period. Aditya Raghunath is a financial "
        "journalist who writes about business, public equities, and personal finance. His work "
        "has been published on several digital platforms in the U.S. and Canada, including The "
        "Motley Fool, Finscreener, and Market Realist. More... Join thousands of investors who "
        "get the latest news, insights and top rated picks from StockNews.com!"
    )
    assert r["created_at"] == "2021-01-13T00:00:00+00:00"
    assert r["tags"] == ["equity", "article", "stocknews.com"]
    assert r["title"] == "Better Buy: NIO vs. GreenPower Motor"
