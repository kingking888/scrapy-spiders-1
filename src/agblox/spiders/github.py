"""Github spider."""
import json
import logging
from typing import Any, Dict, Iterator, Optional

from agblox.items import GithubUserItem
from agblox.settings import AZKA, GHUB_ACCESS_TOKEN
from agblox.spiders.helpers import BaseSpider
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import Response
from scrapy.loader import ItemLoader
from scrapy.settings import Settings

log = logging.getLogger(__name__)


class GithubSpider(BaseSpider):
    """Spider for github.com site."""

    name: str = "github"
    spider_author = AZKA
    config: Optional[str] = None
    download_delay = 1
    access_token = GHUB_ACCESS_TOKEN
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "DiviAIApp/0.1.0 by /u/yugritsai email: yugritsai@gmail.com",
        "Authorization": f"token {GHUB_ACCESS_TOKEN}",
    }

    def __init__(self, *args, **kwargs) -> None:
        """Hide WARNNING log level from validation."""
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.config = kwargs.get("config")
        logger = logging.getLogger("scrapy.core.scraper")
        logger.setLevel(logging.ERROR)

    @classmethod
    def update_settings(cls, settings: Settings) -> None:
        """Customize spider settings."""
        cls.custom_settings["DEFAULT_REQUEST_HEADERS"] = cls.headers
        cls.custom_settings["DOWNLOAD_DELAY"] = cls.download_delay
        settings.setdict(cls.custom_settings or {}, priority="spider")

    def start_requests(self) -> Iterator[scrapy.Request]:
        """This method is called by Scrapy when the spider is opened for scraping.

        We use it to obtain github api response.
        """
        try:
            cfg = self.get_cfg_from_file()
        except Exception as e:
            log.info(f"Can't read configuration from file for [{self.name}]. {e}")

        users = cfg["meta"]["users"]
        for user in users:
            url = f"https://api.github.com/users/{user}"
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_user)

    def parse_user(self, response: Response, **kwargs) -> Any:
        """Parse each returned response of user from Github."""
        if response.status != 200:
            raise CloseSpider(response.body)

        log.info(f"Start fetching information of user: {response.url}")
        data = json.loads(response.body)
        if data:
            # Add user profile basic information to item dict
            item = {}

            item["login_name"] = data["login"]
            item["avatar_url"] = data["avatar_url"]
            item["gravatar_id"] = data["gravatar_id"]
            item["url"] = data["url"]
            item["html_url"] = data["html_url"]
            item["site_admin"] = data["site_admin"]
            item["name"] = data["name"]
            item["company"] = data["company"]
            item["blog"] = data["blog"]
            item["location"] = data["location"]
            item["social_info"] = {
                "twitter_username": data["twitter_username"],
                "contact_email": data["email"],
            }
            item["hireable"] = data["hireable"]
            item["bio"] = data["bio"]
            item["public_repos_count"] = data["public_repos"]
            item["public_gists_count"] = data["public_gists"]
            item["followers_count"] = data["followers"]
            item["following_count"] = data["following"]
            item["created_at"] = data["created_at"]
            item["updated_at"] = data["updated_at"]

            yield scrapy.Request(
                url=data["followers_url"],
                headers=self.headers,
                meta={"item": item},
                callback=self.parse_followers,
                cb_kwargs={"parent_data": data},
            )
        else:
            log.error("Data not found in response", exc_info=True)

    def parse_followers(self, response: Response, **kwargs) -> scrapy.Request:
        """Add user profile followers information to item dict.

        Then make a request to gather user following information.
        """
        log.info(f"Fetching user followers from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        followers = []
        data = json.loads(response.body)
        for follower in data:
            followers.append(follower["login"])
        item["followers"] = followers

        parent_data = kwargs.get("parent_data")
        following_url = parent_data["following_url"].split("{")[0]
        yield scrapy.Request(
            url=following_url,
            headers=self.headers,
            meta={"item": item},
            callback=self.parse_following,
            cb_kwargs={"parent_data": parent_data},
        )

    def parse_following(self, response: Response, **kwargs) -> Any:
        """Add user profile following information to item dict.

        Then make a request to gather user starred information.
        """
        log.info(f"Fetching user followings from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        followings = []
        data = json.loads(response.body)
        for following in data:
            followings.append(following["login"])
        item["followings"] = followings

        parent_data = kwargs.get("parent_data")
        starred_url = parent_data["starred_url"].split("{")[0]
        yield scrapy.Request(
            url=starred_url,
            headers=self.headers,
            meta={"item": item},
            callback=self.parse_starred,
            cb_kwargs={"parent_data": parent_data},
        )

    def parse_starred(self, response: Response, **kwargs) -> Any:
        """Add user starred information to item dict.

        Then make a request to gather user subscriptions information.
        """
        log.info(f"Fetching user starred repos from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        starred_repos = []
        data = json.loads(response.body)
        for starred_repo in data:
            if starred_repo["name"]:
                starred_repos.append(
                    {
                        "name": starred_repo["name"],
                        "description": starred_repo["description"],
                        "language": starred_repo["language"],
                        "topics": starred_repo["topics"],
                    }
                )
        item["starred_repos"] = starred_repos

        parent_data = kwargs.get("parent_data")
        subscriptions_url = parent_data["subscriptions_url"]
        yield scrapy.Request(
            url=subscriptions_url,
            headers=self.headers,
            meta={"item": item},
            callback=self.parse_subscriptions,
            cb_kwargs={"parent_data": parent_data},
        )

    def parse_subscriptions(self, response: Response, **kwargs) -> Any:
        """Add user subscriptions information to item dict.

        Then make a request to gather user organizations information.
        """
        log.info(f"Fetching user subscriptions from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        subscriptions = []
        data = json.loads(response.body)
        for subscription in data:
            if subscription["name"]:
                subscriptions.append(subscription["name"])
        item["subscriptions"] = subscriptions

        parent_data = kwargs.get("parent_data")
        organization_url = parent_data["organizations_url"]
        yield scrapy.Request(
            url=organization_url,
            headers=self.headers,
            meta={"item": item},
            callback=self.parse_organizations,
            cb_kwargs={"parent_data": parent_data},
        )

    def parse_organizations(self, response: Response, **kwargs) -> Any:
        """Add user profile organization information to item dict.

        Then make a request to gather user repositories information.
        """
        log.info(f"Fetching user organizations from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        organizations = []
        data = json.loads(response.body)
        for organization in data:
            members_url = organization["members_url"].split("{")[0]
            repos_url = organization["repos_url"]
            organizations.append(
                {"name": organization["login"], "members": members_url, "repositories": repos_url}
            )
        item["organizations"] = organizations

        if item["organizations"]:
            for each in item["organizations"]:
                request = scrapy.Request(
                    each["members"],
                    headers=self.headers,
                    meta={"item": item},
                    callback=self.parse_organization_members,
                )
                yield request

                request = scrapy.Request(
                    each["repositories"],
                    headers=self.headers,
                    meta={"item": item},
                    callback=self.parse_organization_repositories,
                )
                yield request

        parent_data = kwargs.get("parent_data")
        repos_url = parent_data["repos_url"]
        yield scrapy.Request(
            url=repos_url,
            headers=self.headers,
            meta={"item": item},
            callback=self.parse_repositories,
            cb_kwargs={"parent_data": parent_data},
        )

    def parse_organization_members(self, response: Response, **kwargs) -> Any:
        """Add members information of user organization to item dict."""
        log.info(f"Fetching members of user organization: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        for idx, val in enumerate(item["organizations"]):
            if response.url == val["members"]:
                members = [each["login"] for each in json.loads(response.text)]
                total_members = len(members)
                item["organizations"][idx]["members"] = members
                item["organizations"][idx]["total_members"] = total_members
                return item

    def parse_organization_repositories(self, response: Response, **kwargs) -> Any:
        """Add events information of user organization to item dict."""
        log.info(f"Fetching repositories of user organization: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        for idx, val in enumerate(item["organizations"]):
            if response.url == val["repositories"]:
                item["organizations"][idx]["organization_repositories"] = [
                    each["name"] for each in json.loads(response.text)
                ]
                return item

    def parse_repositories(self, response: Response, **kwargs) -> scrapy.Request:
        """Add user profile repositories information to item dict.

        Then make a request to gather user events information.
        """
        log.info(f"Fetching user repositories from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        repositories = []
        data = json.loads(response.body)
        for repository in data:
            if repository["name"]:
                repo_info = {}
                user = repository["owner"]["login"]
                repo_name = repository["name"]
                repo_info[
                    "technologies"
                ] = f"https://api.github.com/repos/{user}/{repo_name}/languages"
                repo_info[
                    "stargazers"
                ] = f"https://api.github.com/repos/{user}/{repo_name}/stargazers"
                repo_info[
                    "subscribers"
                ] = f"https://api.github.com/repos/{user}/{repo_name}/subscribers"
                repo_info["branches"] = f"https://api.github.com/repos/{user}/{repo_name}/branches"
                repo_info["name"] = repository["name"]
                repo_info["description"] = repository["description"]
                repositories.append(repo_info)

        item["public_repos"] = repositories
        for each in item["public_repos"]:
            request = scrapy.Request(
                each["technologies"],
                headers=self.headers,
                meta={"item": item},
                callback=self.parse_technologies,
            )
            yield request

            request = scrapy.Request(
                each["stargazers"],
                headers=self.headers,
                meta={"item": item},
                callback=self.parse_stargazers,
            )
            yield request

            request = scrapy.Request(
                each["branches"],
                headers=self.headers,
                meta={"item": item},
                callback=self.parse_branches,
            )
            yield request

            request = scrapy.Request(
                each["subscribers"],
                headers=self.headers,
                meta={"item": item},
                callback=self.parse_subscribers,
            )
            yield request

        parent_data = kwargs.get("parent_data")
        events_url = parent_data["events_url"].split("{")[0]
        yield scrapy.Request(
            url=events_url,
            headers=self.headers,
            meta={"item": item},
            callback=self.parse_events,
            cb_kwargs={"parent_data": parent_data},
        )

    def parse_technologies(self, response: Response, **kwargs) -> Any:
        """Add technologies information of user repositories to item dict."""
        log.info(f"Fetching technologies of user repository from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        for idx, val in enumerate(item["public_repos"]):
            if response.url == val["technologies"]:
                item["public_repos"][idx]["technologies"] = list(json.loads(response.text).keys())
                return item

    def parse_stargazers(self, response: Response, **kwargs) -> Any:
        """Add stargazers information of user repositories to item dict."""
        log.info(f"Fetching stargazers of user repository from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        for idx, val in enumerate(item["public_repos"]):
            if response.url == val["stargazers"]:
                item["public_repos"][idx]["stargazers"] = [
                    each["login"] for each in json.loads(response.text)
                ]
                return item

    def parse_branches(self, response: Response, **kwargs) -> Any:
        """Add branches information of user repositories to item dict."""
        log.info(f"Fetching branches of user repository from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        for idx, val in enumerate(item["public_repos"]):
            if response.url == val["branches"]:
                item["public_repos"][idx]["branches"] = [
                    each["name"] for each in json.loads(response.text)
                ]
                return item

    def parse_subscribers(self, response: Response, **kwargs) -> Any:
        """Add subscribers information of user repositories to item dict."""
        log.info(f"Fetching subscribers of user repository from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        for idx, val in enumerate(item["public_repos"]):
            if response.url == val["subscribers"]:
                item["public_repos"][idx]["subscribers"] = [
                    each["login"] for each in json.loads(response.text)
                ]
                return item

    def parse_events(self, response: Response, **kwargs) -> Any:
        """Add user received events information to item dict.

        Then make a request to gather user received events information.
        """
        log.info(f"Fetching user events from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        events_count = 0
        events = []
        data = json.loads(response.body)
        if len(data) > 0:
            events_count = len(data)
            for event in data:
                organization = ""
                if "org" in event:
                    organization = event["org"]["login"]

                events.append(
                    {
                        "type": event["type"],
                        "public": event["public"],
                        "user": event["actor"]["login"],
                        "repository": event["repo"]["name"],
                        "organization": organization,
                    }
                )
        item["events_count"] = events_count
        item["events"] = events

        parent_data = kwargs.get("parent_data")
        recieved_event_url = parent_data["received_events_url"]
        yield scrapy.Request(
            url=recieved_event_url,
            headers=self.headers,
            meta={"item": item},
            callback=self.parse_received_events,
            cb_kwargs={"parent_data": parent_data},
        )

    def parse_received_events(self, response: Response, **kwargs) -> Any:
        """Add user events information to item dict.

        Then make a request to gather user projects information.
        """
        log.info(f"Fetching user received events from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        events_count = 0
        events = []
        data = json.loads(response.body)
        if len(data) > 0:
            events_count = len(data)
            for event in data:
                organization = ""
                if "org" in event:
                    organization = event["org"]["login"]

                events.append(
                    {
                        "type": event["type"],
                        "public": event["public"],
                        "user": event["actor"]["login"],
                        "repository": event["repo"]["name"],
                        "organization": organization,
                    }
                )
        item["received_events_count"] = events_count
        item["received_events"] = events

        parent_data = kwargs.get("parent_data")
        projects_url = item["url"] + "/projects"
        yield scrapy.Request(
            url=projects_url,
            headers=self.headers,
            meta={"item": item},
            callback=self.parse_projects,
            cb_kwargs={"parent_data": parent_data},
        )

    def parse_projects(self, response: Response, **kwargs) -> Any:
        """Add user projects information to item dict.

        Also call the add_item to add the final item to ItemLoader.
        """
        log.info(f"Fetching user projects from url: {response.url}")
        if response.status != 200:
            raise CloseSpider(response.body)
        item = response.meta["item"]

        projects = []
        data = json.loads(response.body)
        for project in data:
            projects.append(project["name"])
        item["projects"] = projects

        # TODO: By similar calls, gather remaining user profile data like projects
        yield self.add_item(item)

    @staticmethod
    def add_item(item: Dict) -> Any:
        """Method for add item to ItemLoader."""
        try:
            loader = ItemLoader(item=GithubUserItem())
            loader.add_value("url", item["url"])
            loader.add_value(
                "meta",
                {
                    "login_name": item["login_name"],
                    "avatar_url": item["avatar_url"],
                    "gravatar_id": item["gravatar_id"],
                    "html_url": item["html_url"],
                    "followers": item["followers"],
                    "followings": item["followings"],
                    "starred_repos": item["starred_repos"],
                    "subscriptions": item["subscriptions"],
                    "organizations": item["organizations"],
                    "public_repos": item["public_repos"],
                    "events": item["events"],
                    "received_events": item["received_events"],
                    "projects": item["projects"],
                    "site_admin": item["site_admin"],
                    "name": item["name"],
                    "company": item["company"],
                    "blog": item["blog"],
                    "location": item["location"],
                    "social_info": item["social_info"],
                    "hireable": item["hireable"],
                    "bio": item["bio"],
                    "public_repos_count": item["public_repos_count"],
                    "public_gists_count": item["public_gists_count"],
                    "followers_count": item["followers_count"],
                    "following_count": item["following_count"],
                    "events_count": item["events_count"],
                    "received_events_count": item["received_events_count"],
                    "created_at": item["created_at"],
                    "updated_at": item["updated_at"],
                },
            )

            log.info(f"Downloaded Github's item: {item['url']}. Adding...")
            return loader.load_item()
        except Exception as e:
            log.error(f"Was problem with: {item['url']}. Error: {e}", exc_info=True)
            return None
