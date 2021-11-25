from dataclasses import dataclass

from .clients import BaseClient, MediaWiki, MediaWiki_Lurk
from .drivers import HttpxDriver
from .models import URL
from .exceptions import NotFound


@dataclass
class Wikipya:
    lang: str = "ru"
    base_url: str = "https://{lang}.wikipedia.org/w/api.php"
    prefix: str = "/w"
    client: BaseClient = MediaWiki
    is_lurk: bool = False
    img_blocklist: list = ()

    def __post_init__(self):
        self.url = URL(self.base_url, self.lang, self.prefix)

        self.client = MediaWiki_Lurk if self.is_lurk else self.client
        self.client = self.client(url=self.url, prefix=self.prefix, driver=HttpxDriver,
                                  img_blocklist=self.img_blocklist)

    def get_instance(self) -> MediaWiki:
        return self.client
