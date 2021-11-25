from params import Params


def test_https(params: Params):
    # Use HTTPS instead of HTTP, please. Ignore with ALLOW_HTTP
    wiki = params.client

    is_https_used = wiki.url.base_url.startswith("https://")
    assert params.allow_http or is_https_used
