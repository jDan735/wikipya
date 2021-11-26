from .base import BaseClient
from ..models import Page, Search, SearchResult, Image, OpenSearch, Summary
from ..exceptions import NotFound


class MediaWiki(BaseClient):
    WGR_FLAG = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb" +
        "/8/85/Flag_of_Belarus.svg/1000px-Flag_of_Belarus.svg.png"
    )

    WRW_FLAG = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb" +
        "/5/50/Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg" +
        "/1000px-Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg.png"
    )

    LANG = None

    async def search(self, query, limit=1, prop="snippet") -> list[SearchResult]:
        res = await self.driver.get(
            list="search",
            srsearch=query,
            srlimit=limit,
            srprop=prop
        )

        results = Search.parse_obj(res.json["query"]["search"]).__root__

        if len(results) == 0:
            raise NotFound("Search can't find anything on your request")
        else:
            return results

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

    async def page(self, query, section=0, prop="text", blocklist=()) -> Page:
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

        try:
            res.json["parse"]["text"] = res.json["parse"]["text"]["*"]
        except Exception:
            pass

        page = Page.parse_obj(res.json["parse"])
        page.tag_blocklist = blocklist

        return page

    async def summary(self, title) -> Summary:
        res = await self.driver.get_html(
            f"{self.driver.url.cleaned}api/rest_v1/page/summary/{title}")

        return Summary.parse_raw(res.text)

    async def image(self, titles, pithumbsize=1000, img_blocklist=()) -> Image:
        res = await self.driver.get(
            titles=titles,
            prop="pageimages",
            pilicense="any",
            pithumbsize=pithumbsize,
            piprop="thumbnail",
        )

        try:
            image = res.json["query"]["pages"][-1]
            thumb = image["thumbnail"]

            return Image(**thumb)
        except AttributeError:
            raise NotFound("Not found image")

    async def get_page_name(self, id) -> str:
        res = await self.driver.get(pageids=id)

        try:
            return res.json["query"]["pages"][-1]["title"]
        except AttributeError:
            raise NotFound(f"Not found page with this id: {id}")

    async def get_all(self, query, lurk=False,
                      blocklist=(), prefix="w", img_blocklist=(), **kwargs):
        search = await self.search(query)
        opensearch = await self.opensearch(
            query if lurk else search[0].title
        )

        result = opensearch.results[0]
        page = await self.page(result.title, blocklist=blocklist)

        try:
            image = await self.image(page.title, prefix=prefix, img_blocklist=img_blocklist)
            image = image.source

        except Exception:
            image = -1

        if image == self.WGR_FLAG:
            image = self.WRW_FLAG

        return page, image, result.link
