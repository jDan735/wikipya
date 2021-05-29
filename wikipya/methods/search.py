from .base import BaseContoller
from ..exceptions import NotFound
from ..types.search import SearchItem


class Search(BaseContoller):
    METHODS = {
        "search": ">=1.0"
    }

    async def search(self, query, limit, prop="size", **kwargs):
        status, data = await self.driver.get(
            list="search",
            srsearch=query,
            srlimit=limit,
            srprop=prop,
            **kwargs
        )

        if len(data.query.search) == 0:
            raise NotFound("Search can't find anything on your request")

        return [SearchItem(
            title=item.title,
            pageid=item.pageid
        ) for item in data.query.search]
