"""https://fallout.fandom.com/ru/wikia.php
?controller=UnifiedSearchSuggestions
&method=getSuggestions
&query=%D0%BC%D0%B5%D0%B3%D0%B0%D1%82%D0%BE%D0%BD%D0%BD%D0%B0
&format=json
&scope=internal"""

from ..exceptions import NotFound

from typing import TYPE_CHECKING
from ..models import Suggestion, QuickSearchResults

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def fandom_search(
    self: "MediaWikiAbstract", query: str, limit: int = 1
) -> list[Suggestion]:
    _, json = await self.get(
        url=self.url.url.replace("api.php", "wikia.php"),
        query=query,
        limit=limit,
        # FANDOM SHIT
        controller="UnifiedSearchSuggestions",
        method="getSuggestions",
        scope="internal",
    )

    if len(json["suggestions"]) == 0:
        raise NotFound("Search can't find anything on your request")

    sugs: list[Suggestion] = []

    for name in json["suggestions"]:
        id = json["ids"][name]
        image = json["images"][str(id)]

        sugs.append(Suggestion(page_id=id, title=name, image=image))

    results = QuickSearchResults(sugs[:limit])  # type: ignore

    return results.root
