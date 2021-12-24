from ..models import OpenSearch
from ..exceptions import NotFound


async def opensearch(self, query, limit=1) -> OpenSearch:
    r = await self.driver.get(
        action="opensearch",
        search=query,
        limit=limit,
    )

    results = OpenSearch(*r.json)

    if len(results.results) == 0:
        raise NotFound("OpenSearch can't find anything on your request")

    return results
