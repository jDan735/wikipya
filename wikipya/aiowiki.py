from dataclasses import dataclass, field

from .clients import BaseClient, MediaWiki, MediaWiki_Lurk
from .drivers import HttpxDriver
from .models import URL
from .exceptions import NotFound  # noqa


@dataclass
class Wikipya:
    lang: str = "ru"
    base_url: str = "https://{lang}.wikipedia.org/w/api.php"
    prefix: str = "/w"

    client: BaseClient = MediaWiki
    is_lurk: bool = False

    params: dict = field(default_factory=dict)

    def __post_init__(self):
        self.url = URL(self.base_url, self.lang, self.prefix)

        self.client = MediaWiki_Lurk if self.is_lurk else self.client
        self.client = self.client(
            url=self.url,
            driver=HttpxDriver,

            **self.params
        )

    def get_instance(self) -> MediaWiki:
        return self.client
