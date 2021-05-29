from .base import BaseContoller
from ..exceptions import NotFound


class OpenSearch(BaseContoller):
    METHODS = {
        "opensearch": ">=1.0"
    }

    async def opensearch(self, query, limit, **kwargs):
        status, data = await self.driver.get(
            action="opensearch",
            search=query,
            limit=limit,
            **kwargs
        )

        if len(data) == 0:
            raise NotFound("Search can't find anything on your request")

        return data
