from typing import Optional

from msgspec import Struct


class OpenSearch(Struct, frozen=True, array_like=True):
    query: str
    titles: list[str]
    descriptions: list[str]
    links: list[str]

    def prettify(self) -> list[OpenSearchResult]:
        return [
            OpenSearchResult(title, self.links[i])
            for i, title in enumerate(self.titles)
        ]


class OpenSearchResult(Struct, frozen=True):
    title: str
    link: str | None = None
