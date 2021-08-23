from dataclasses import dataclass, field
from typing import Any

from tghtml import TgHTML

from .drivers import JSONObject


@dataclass
class SearchItem:
    title: str
    pageid: int


@dataclass
class OpenSearchResult:
    query: str
    _variants: list
    unknown: list = field(default_factory=list)
    links: list = field(default_factory=list)
    variants: Any = field(default_factory=list)

    def __post_init__(self):
        for i, variant in enumerate(self._variants):
            link = self.links[i] if len(self.links) > 0 else None

            self.variants.append(OpenSearchItem(variant, link))


@dataclass
class OpenSearchItem:
    title: str
    link: str = None


@dataclass
class Image:
    source: str
    width: int
    height: int

    def __post_init__(self):
        if self.source.find(".gif") != -1:
            raise TypeError("Gif file")

        if self.source.find("revision/latest/scale-to-width-down") != -1:
            revision = self.source.split("/revision")
            rev = revision[1].split("?")[0]
            size = rev.split("/")[-1]

            new_rev = rev.replace(str(size), "10000")

            self.source = self.source.replace(rev, new_rev)


@dataclass
class WikipyaPage:
    parse: JSONObject
    lang: str = "en"
    tag_blocklist: tuple = ()
    img_blocklist: tuple = ()
    _image: Any = None

    def __post_init__(self):
        vars(self).update(self.parse.__dict__)

        # fix for lurkmore
        if self.text.__class__.__name__ == "JSONObject":
            self.text = self.text.__dict__["*"]

    async def image(self, *args, **kwargs):
        return await self._image(self.title, *args, **kwargs)

    @property
    def parsed(self):
        return str(TgHTML(self.text, self.tag_blocklist, is_wikipedia=False))

    @property
    def fixed(self):
        namelist = [
            ["Белоруссия", "Беларусь"],
            ["Белоруссии", "Беларуси"],
            ["Беларуссию", "Беларусь"],
            ["Белоруссией", "Беларусью"],
            ["Белоруссиею", "Беларусью"],

            ["Белору́ссия", "Белару́сь"],
            ["Белору́ссии", "Белару́си"],
            ["Белору́ссию", "Белару́сь"],
            ["Белору́ссией", "Белару́сью"],
            ["Белору́ссиею", "Белару́сью"],


            ["на Украин", "в Украин"],
        ]

        for name in namelist:
            text = self.parsed.replace(*name)

        return text