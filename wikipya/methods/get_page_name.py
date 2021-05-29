from .base import BaseContoller
from ..exceptions import NotFound


class GetPageName(BaseContoller):
    METHODS = {
        "getPageName": ">=1.0"
    }

    async def getPageName(self, id_):
        status, data = await self.driver.get(
            pageids=id_
        )

        try:
            return data.query.pages[-1].title
        except AttributeError:
            raise NotFound(f"Not found page with this id: {id_}")
