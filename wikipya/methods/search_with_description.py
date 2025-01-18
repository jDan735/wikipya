from ..models import SearchWithDescription, SearchResultWithDescripion
from ..exceptions import NotFound

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def search_with_description(
    self: "MediaWikiAbstract", query: str, limit: int = -1, pithumbsize: int = 200
) -> list[SearchResultWithDescripion]:
    _, json = await self.get(
        generator="prefixsearch",
        prop="pageprops|pageimages|description",
        redirects="",
        ppprop="displaytitle",
        piprop="thumbnail",
        pithumbsize=pithumbsize,
        plimit=limit,
        gpssearch=query,
        gpsnamespace=0,
        gpslimit=limit,
    )

    results_raw = sorted(json["query"]["pages"], key=lambda x: x["index"])
    results = SearchWithDescription.model_validate(results_raw).root

    if len(results) == 0:
        raise NotFound("Search can't find anything on your request")
    else:
        return results
