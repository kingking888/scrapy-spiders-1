"""Module used for overriding default rotating_proxies.policy import BanDetectionPolicy."""

from typing import Any

from rotating_proxies.policy import BanDetectionPolicy
from scrapy.exceptions import IgnoreRequest
from scrapy.http import Request, Response


class AgBloxBanPolicy(BanDetectionPolicy):
    """Custom ban policy."""

    NOT_BAN_STATUSES = {200, 201, 301, 302}
    NOT_BAN_EXCEPTIONS = (IgnoreRequest,)

    def response_is_ban(self, request: Request, response: Response) -> Any:
        """Detects if returned response is ban."""
        # use default rules, but also consider HTTP 200 responses
        # a ban if there is 'captcha' word in response body.
        ban = super(AgBloxBanPolicy, self).response_is_ban(request, response)
        ban = ban or b"captcha" in response.body
        return ban

    def exception_is_ban(self, request: Request, exception: Exception) -> Any:
        """Detects if caused exception is a ban."""
        # override method completely: don't take exceptions in account
        return None
