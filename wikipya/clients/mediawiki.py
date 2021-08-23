from .base import BaseClient
from ..types import SearchItem, WikipyaPage, Image, OpenSearchResult

from ..exceptions import NotFound


class MediaWiki(BaseClient):
    DEFAULT_PARAMS = {
        "format": "json",
        "action": "query",
        "formatversion": 2
    }

    BASE_URL = "https://{lang}.wikipedia.org/w/api.php"
    LANG = None

    WGR_FLAG = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb" +
        "/8/85/Flag_of_Belarus.svg/1000px-Flag_of_Belarus.svg.png"
    )

    WRW_FLAG = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb" +
        "/5/50/Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg" +
        "/1000px-Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg.png"
    )

    async def search(self, query, limit=1, prop="size"):
        res = await self.driver.get(
            list="search",
            srsearch=query,
            srlimit=limit,
            srprop=prop
        )

        if len(res.query.search) == 0:
            raise NotFound("Search can't find anything on your request")

        return [SearchItem(
            title=item.__dict__.get("title"),
            pageid=item.__dict__.get("pageid")
        ) for item in res.query.search]

    async def opensearch(self, query, limit=1):
        res = OpenSearchResult(*await self.driver.get(
            action="opensearch",
            search=query,
            limit=limit,
        ))

        if len(res.variants) == 0:
            raise NotFound("OpenSearch can't find anything on your request")

        return res

    async def page(self, query, section=0, prop="text", blocklist=()):
        if query.__class__ == str:
            params = {"page": query}

        elif query.__class__ == int:
            params = {"pageid": query}

        elif query.pageid is not None:
            params = {"pageid": query.pageid}

        else:
            params = {"page": query.title}

        res = await self.driver.get(
            action="parse",
            section=section,
            prop=prop,
            redirects="true",
            **params,
        )

        return WikipyaPage(res.parse, lang=self.LANG, _image=self.image,
                           tag_blocklist=blocklist)

    async def image(self, titles, pithumbsize=1000,
                    piprop="thumbnail", img_blocklist=(), prefix=None):
        res = await self.driver.get(
            titles=titles,
            prop="pageimages",
            pilicense="any",
            pithumbsize=pithumbsize,
            piprop=piprop,
        )

        try:
            image = res.query.pages[-1]
            thumb = image.thumbnail

            return Image(**thumb.__dict__)

        except AttributeError:
            raise NotFound("Not found image")

    async def getPageName(self, id_):
        res = await self.driver.get(
            pageids=id_
        )

        try:
            return res.query.pages[-1].title
        except AttributeError:
            raise NotFound(f"Not found page with this id: {id_}")

    async def get_all(self, query, lurk=False,
                      blocklist=(), prefix="w", img_blocklist=(), **kwargs):
        search = await self.search(query)
        opensearch = await self.opensearch(
            query if lurk else search[0].title
        )

        variant = opensearch.variants[0]
        page = await self.page(variant.title, blocklist=blocklist)

        try:
            image = await page.image(prefix=prefix,
                                     img_blocklist=img_blocklist)
            image = image.source

        except Exception as e:
            image = -1

        if image == self.WGR_FLAG:
            image = self.WRW_FLAG

        return page, image, variant.link
