from ..models import SearchWithDescription, SearchResultWithDescripion
from ..exceptions import NotFound


async def search_with_description(
    self,
    query: str,
    limit: int = -1,
    pithumbsize: int = 200
) -> list[SearchResultWithDescripion]:
    res = await self.driver.get(
        generator="prefixsearch",
        prop="pageprops|pageimages|description",
        redirects="",
        ppprop="displaytitle",
        piprop="thumbnail",
        pithumbsize=pithumbsize,
        plimit=limit,
        gpssearch=query,
        gpsnamespace=0,
        gpslimit=limit
    )

    results_raw = sorted(res.json["query"]["pages"], key=lambda x: x["index"])
    results = SearchWithDescription.model_validate(results_raw).root

    if len(results) == 0:
        raise NotFound("Search can't find anything on your request")
    else:
        return results
