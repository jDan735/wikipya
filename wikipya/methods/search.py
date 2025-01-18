from ..exceptions import NotFound
from ..models.suggestion import QuickSearchResults, Suggestion

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def search(
    self: "MediaWikiAbstract", query: str, limit: int = 1, prop: str = "snippet"
) -> list[Suggestion]:
    _, json = await self.get(list="search", srsearch=query, srlimit=limit, srprop=prop)

    results = QuickSearchResults.model_validate(json["query"]["search"]).root

    if len(results) == 0:
        raise NotFound("Search can't find anything on your request")
    else:
        return results
