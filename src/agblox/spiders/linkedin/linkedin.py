"""Linkedin spider."""
from abc import ABC
import datetime
import logging
from typing import Iterator, List

from agblox.items import LinkedinItem
from agblox.settings import DANIYAL, LINKEDIN_EMAIL, LINKEDIN_PASSWORD
from agblox.spiders.helpers import BaseSpider
from agblox.spiders.linkedin.data import corpus
from linkedin_api import Linkedin
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

log = logging.getLogger(__name__)


class LinkedinSpider(BaseSpider, ABC):
    """Spider for linkedin.com site."""

    name: str = "linkedin"
    tags: List[str] = ["alpha", "bravo", "charlie"]
    host_header = "www.linkedin.com"
    spider_author = DANIYAL

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping.

        This method just placeholder.
        """
        yield scrapy.Request(
            url="https://www.linkedin.com/",
            callback=self.query_api,
        )

    def query_api(self, response: TextResponse, **kwargs) -> Iterator[LinkedinItem]:
        """Parse navigation page.

        This is the default callback used by Scrapy to process downloaded responses, when
        their requests don’t specify a callback.
        """
        api = Linkedin(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
        if response.status != 200:
            raise CloseSpider(response.body)
        for item in corpus:
            company = self._clean_company_name(item[2])
            response = api.search_people(item[1] + " CEO " + company)
            if response:
                for name in response:
                    username = name.get("public_id")
                    complete_profile = api.get_profile(username)

                    loader = ItemLoader(item=LinkedinItem())
                    loader.add_value("name", item[1])
                    loader.add_value("profile_id", username)
                    loader.add_value("position", "Chief Executive Officer")
                    loader.add_value("url", "https://linkedin.com/in/%s" % username)
                    loader.add_value("meta", complete_profile)
                    loader.add_value("tags", self.tags)
                    loader.add_value(
                        "scraped_at",
                        datetime.datetime.utcnow()
                        .replace(tzinfo=datetime.timezone.utc)
                        .isoformat(),
                    )
                    loader.add_value(
                        "updated_at",
                        datetime.datetime.utcnow()
                        .replace(tzinfo=datetime.timezone.utc)
                        .isoformat(),
                    )
                    loader.add_value("person_identifier", item[0])
                    self.logger.info("Adding profile: %s" % username)

                    yield loader.load_item()

    @staticmethod
    def _clean_company_name(company: str) -> str:
        grey_list = ["co.", "corp", "group", "holding", "inc", "llc", "plc"]
        company_name = company.split()
        blacklist = []
        for word in company_name[1:]:
            for not_allowed in grey_list:
                if word.lower().find(not_allowed) == 0:
                    blacklist.append(word)
        for not_allowed in blacklist:
            company_name.remove(not_allowed)
        return " ".join(company_name)
