from .clients import BaseClient, MediaWiki, MediaWikiAbstract
from .drivers import HttpxDriver
from .models import URL


def Wikipya(
    lang: str = "ru",
    base_url: str = "https://{lang}.wikipedia.org/w/api.php",
    prefix: str = "/w",
    client: BaseClient = MediaWiki,
    params: dict = dict(),
) -> MediaWikiAbstract:
    print(base_url)
    return client(url=URL(base_url, lang, prefix), driver=HttpxDriver, **params)
