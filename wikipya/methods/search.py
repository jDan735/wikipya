from ..models import SearchResult
from ..exceptions import NotFound
from ..models.suggestion import QuickSearchResults


async def search(self, query, limit=1, prop="snippet") -> list[SearchResult]:
    res = await self.driver.get(
        list="search", srsearch=query, srlimit=limit, srprop=prop
    )

    results = QuickSearchResults.model_validate(res.json["query"]["search"]).root

    if len(results) == 0:
        raise NotFound("Search can't find anything on your request")
    else:
        return results
