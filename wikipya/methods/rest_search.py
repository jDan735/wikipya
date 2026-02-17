from ..exceptions import NotFound
from ..models.suggestion import QuickSearchResults, Suggestion

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def rest_search(
    self: "MediaWikiAbstract",
    query: str,
    limit: int = 1,
    prop: str = "",
) -> list[Suggestion]:
    _, json = await self.get(
        self.url.cleaned + "/w/rest.php/v1/search/title",
        q=query,
        limit=limit,
    )

    __ = [
        {
            "page_id": page["id"],
            "title": page["title"],
        }
        for page in json["pages"]
    ]

    results = QuickSearchResults.model_validate(__).root

    if len(results) == 0:
        raise NotFound("Search can't find anything on your request")
    else:
        return results
