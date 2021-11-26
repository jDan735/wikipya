from dataclasses import dataclass, field
from typing import Any


@dataclass
class OpenSearch:
    query: str
    _variants: list = field(default_factory=list, repr=False)
    descriptions: list = field(default_factory=list, repr=False)
    links: list = field(default_factory=list, repr=False)
    results: Any = field(default_factory=list)

    def __post_init__(self):
        for i, variant in enumerate(self._variants):
            link = self.links[i] if len(self.links) > 0 else None

            self.results.append(OpenSearchResult(variant, link))


@dataclass
class OpenSearchResult:
    title: str
    link: str = None
