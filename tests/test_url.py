import pytest
from params import Params


def test_https(params: Params):
    # Use HTTPS instead of HTTP, please. Ignore with ALLOW_HTTP

    is_https_used = params.client.url.startswith("https://")
    assert params.allow_http or is_https_used
