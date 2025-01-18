from pydantic.dataclasses import dataclass
from pydantic import Field
from typing import Optional


@dataclass
class OpenSearch:
    query: str
    _variants: list[str] = Field(default_factory=list, repr=False)
    descriptions: list[str] = Field(default_factory=list, repr=False)
    links: list[str] = Field(default_factory=list, repr=False)
    results: list["OpenSearchResult"] = Field(default_factory=list)

    def __post_init__(self):
        for i, variant in enumerate(self._variants):
            link = self.links[i] if len(self.links) > 0 else None

            self.results.append(OpenSearchResult(variant, link))


@dataclass
class OpenSearchResult:
    title: str
    link: Optional[str] = None
