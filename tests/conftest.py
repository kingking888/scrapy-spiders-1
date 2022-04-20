"""Package-wide test fixtures and pytest hooks"""

import os
import re
from typing import List, Optional

# flake8: noqa: DAR101 DAR201
from _pytest.config import Config
import pytest
import requests
import scrapy
import vcr


def pytest_assertrepr_compare(
    config: Config, op: str, left: str, right: str
) -> Optional[List[str]]:
    """Hook for PyCharm full diff fix.

    References:
        https://stackoverflow.com/a/50625086/4249707
    """
    if op in ("==", "!="):
        return ["{0} {1} {2}".format(left, op, right)]


# modified https://github.com/tcurvelo/scrapy-mock


def slugify(request):
    name = request.node.name
    name = re.sub(r"(?:\])", "", name)
    name = re.sub(r"(?:\[|-)", "__", name)
    name = re.sub(r"[:/\.?&=]+", "-", name)
    if request.cls:
        return f"{request.cls}.{name}"
    else:
        return name


@pytest.fixture(scope="session")
def vcr_settings():
    # Avoid HTTP requests in CI environments.
    # (Bitbucket, Gitlab and Travis use `CI=true` as default)
    record_mode = "none" if os.getenv("CI") else "once"
    return vcr.VCR(
        decode_compressed_response=True,
        cassette_library_dir="tests/fixtures/cassettes",
        record_mode=record_mode,
    )


@pytest.fixture()
def response(request, vcr_settings, url, headers):
    filename = slugify(request)
    session = MockSession()
    with vcr_settings.use_cassette(f"{filename}.yaml"):
        yield session.get(url, headers=headers)


class MockSession(requests.Session):
    def get(self, url, meta=None, headers=None):
        return self._request("GET", url, meta, headers)

    def _request(self, method, url, meta=None, headers=None, **kwargs):
        response = super(MockSession, self).request(method, url, headers=headers, **kwargs)
        return scrapy.http.HtmlResponse(
            body=response.content, url=url, request=scrapy.http.Request(url, cb_kwargs=meta)
        )
