from .base import BaseContoller
from ..types.page import WikipyaPage


class Page(BaseContoller):
    METHODS = {
        "page": ">=1.0"
    }

    async def page(self, query, section=0, prop="text",
                   params={}, **kwargs):
        if query.__class__ == str:
            params = {"page": query}

        elif query.__class__ == int:
            params = {"pageid": query}

        else:
            params = {"pageid": query.pageid}

        status, data = await self.driver.get(
            action="parse",
            section=section,
            prop=prop,
            **params,
            **kwargs
        )

        return WikipyaPage(data.parse, lang=self.lang,
                           params=self)

    async def _page(self, query, exsentences=5, params={}, **kwargs):
        if exsentences == -1:
            exsentences_json = {}
        else:
            exsentences_json = {"exsentences": exsentences}

        status, data = await self.driver.get(
            prop="extracts",
            titles=query.title,
            formatversion=1,
            **exsentences_json
        )

        result = data.query.pages.__dict__

        if "-1" in result:
            return -1

        query = result[list(result.keys())[-1]]
        query.add({"text": query.extract})

        return WikipyaPage(query, lang=self.lang, params=params)
