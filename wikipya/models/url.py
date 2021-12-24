import re

from dataclasses import dataclass
from typing import Optional


@dataclass
class URL:
    base_url: str = "https://{lang}.wikipedia.org/w/api.php"
    lang: Optional[str] = "ru"
    prefix: str = "/w"

    def __str__(self):
        return self.url

    @property
    def url(self):
        return self.base_url.format(lang=self.lang)

    @property
    def image_url(self):
        return re.sub(r"(wiki|w)?/api.php", self.prefix, self.url)

    @property
    def cleaned(self):
        return re.sub(r"(wiki|w)?/api.php", "", self.url)
