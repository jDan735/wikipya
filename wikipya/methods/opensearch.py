from ..models import OpenSearch, OpenSearchResult
from ..exceptions import NotFound

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def opensearch(
    self: "MediaWikiAbstract", query: str, limit: int = 1
) -> list[OpenSearchResult]:
    _, res = await self.get(
        action="opensearch",
        search=query,
        limit=limit,
        type=OpenSearch,
    )
    results = res.prettify()

    if len(results) == 0:
        raise NotFound("OpenSearch can't find anything on your request")

    return results
