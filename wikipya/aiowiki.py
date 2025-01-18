from typing import Any
from .clients import MediaWiki, Fandom, Wikipedia, MediaWikiAbstract
from .models import MediawikiUrl

from httpx import URL


def Wikipya(
    lang: str = "ru",
    base_url: str = "https://{lang}.wikipedia.org/w/api.php",
    prefix: str = "/w",
    params: dict[Any, Any] = {},
) -> MediaWikiAbstract:
    match URL(base_url).host.split(".")[-2]:
        case "wikipedia":
            client = Wikipedia
        case "fandom":
            client = Fandom
        case _:
            client = MediaWiki

    return client(url=MediawikiUrl(base_url, lang, prefix), **params)  # type: ignore
