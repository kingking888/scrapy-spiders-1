"""Intrinio Weekly spider."""
import logging
from typing import Iterator, List

from agblox.items import ModelDataItem
from agblox.settings import AZKA, INTRINIO_API_KEY
from agblox.spiders.helpers import ModelDataSpider
import intrinio_sdk as intrinio
from intrinio_sdk.rest import ApiException
import scrapy
from scrapy import Request
from scrapy.http import Response

log = logging.getLogger(__name__)


class IntrinioWeeklySpider(ModelDataSpider):
    """Spider for intrinio weekly data."""

    spider_author = AZKA
    name: str = "intrinio_weekly"
    host_header = "docs.intrinio.com"
    s3_dir_key = "companies-models-data/intrinio-weekly/"
    file_prefix = "intrinio_weekly_"
    extra_vars = [
        "marketcap",
        "evtoebitda",
        "enterprisevalue",
        "dividendyield",
        "pricetoearnings",
        "earningsyield",
        "pricetobook",
        "evtorevenue",
        "evtoinvestedcapital",
        "evtofcff",
        "pricetorevenue",
        "pricetotangiblebook",
    ]

    custom_settings = {
        "ITEM_PIPELINES": {
            "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline": 300,
            "agblox.pipelines.FSIntrinioDataPipeline": 310,
            "agblox.pipelines.S3IntrinioDataPipeline": 320,
            "agblox.pipelines.APIPipelineReport": 350,
            "agblox.pipelines.NotifierPipeline": 500,
        }
    }

    def load_tickers(self) -> List:
        """Function will load tickers from s3 bucket."""
        tickers500 = self.fetch_tickers_from_s3()
        spy = tickers500[0]["SPY"]
        return spy

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping."""
        yield Request("https://docs.intrinio.com/documentation/python")

    def parse(self, response: Response, **kwargs) -> scrapy.Request:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        intrinio.ApiClient().set_api_key(INTRINIO_API_KEY)
        intrinio.ApiClient().allow_retries(True)
        tickers500 = self.load_tickers()

        for ticker in tickers500:
            try:
                extrvrs = {k: [] for k in self.extra_vars}
                for fin in self.extra_vars:
                    identifier = ticker
                    tag = fin
                    frequency = "weekly"
                    type1 = ""
                    start_date = "2018-01-01"
                    end_date = ""
                    sort_order = "desc"
                    page_size = 10000
                    next_page = ""

                    response = intrinio.HistoricalDataApi().get_historical_data(
                        identifier,
                        tag,
                        frequency=frequency,
                        type=type1,
                        start_date=start_date,
                        end_date=end_date,
                        sort_order=sort_order,
                        page_size=page_size,
                        next_page=next_page,
                    )
                    log.info("Fetched data for %s | ticker: %s" % (fin, ticker))
                    for i in response.historical_data_dict:
                        i = {"date": str(i["date"]), "value": i["value"]}
                        extrvrs[fin].append(i)
                item = ModelDataItem(data={ticker: extrvrs}, ticker=ticker)
                yield item

            except ApiException:
                continue
            except ValueError:
                continue
