from ..models import OpenSearch
from ..exceptions import NotFound

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def opensearch(
    self: "MediaWikiAbstract", query: str, limit: int = 1
) -> OpenSearch:
    _, json = await self.get(
        action="opensearch",
        search=query,
        limit=limit,
    )

    results = OpenSearch(*json)

    if len(results.results) == 0:
        raise NotFound("OpenSearch can't find anything on your request")

    return results
