from .drivers import AiohttpDriver
from .exceptions import NotFound

from .methods.image import ImageController

from .types.page import WikipyaPage
from .types.image import Image
from .types.search import SearchItem


class Wikipya:
    def __init__(
        self, lang=None, driver=AiohttpDriver, version="1.0",
        url="https://{lang}.wikipedia.org/w/api.php", params={
            "format": "json",
            "action": "query",
            "formatversion": 2
        }, img_blocklist=(), host=""
    ):
        """ Initialisation instance of Wikipya
        Args:
            lang: Lang of MediaWiki source
            driver: Driver for connection to service
            version: Version of MediaWiki
            url: Template of URL to wiki
            params: Default params for driver
            img_blocklist: List ignored images (lurk patch)
        """

        self.MEDIAWIKI_VERSION = version

        self.img_blocklist = img_blocklist
        self.lang = lang
        self.url = url if lang is None else url.format(
            lang=self.lang
        )
        self.host = host

        self.driver = driver(url=self.url,
                             params=params)

    @property
    def params(self):
        return {
            "lang": self.lang,
            "driver": self.driver,
            "version": self.MEDIAWIKI_VERSION,
            "url": self.url,
            "host": self.host
        }

    async def search(self, query, limit=1, prop="size", **kwargs):
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
            title=item.__dict__.get("title"),
            pageid=item.__dict__.get("pageid")
        ) for item in data.query.search]

    async def opensearch(self, query, limit=1, **kwargs):
        status, data = await self.driver.get(
            action="opensearch",
            search=query,
            limit=limit,
            **kwargs
        )

        if len(data) == 0:
            raise NotFound("Search can't find anything on your request")

        return data

    async def page(self, query, section=0, prop="text",
                   params={}, **kwargs):
        if query.__class__ == str:
            params = {"page": query}

        elif query.__class__ == int:
            params = {"pageid": query}

        elif query.pageid is not None:
            params = {"pageid": query.pageid}

        else:
            params = {"page": query.title}

        status, data = await self.driver.get(
            action="parse",
            section=section,
            prop=prop,
            redirects="true",
            **params,
            **kwargs
        )

        return WikipyaPage(data.parse, lang=self.lang,
                           img_blocklist=self.img_blocklist,
                           params=self.params)

    async def _page(self, query, exsentences=5, section=0,
                    params={}, **kwargs):
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

        return WikipyaPage(query, lang=self.lang, 
                           img_blocklist=self.img_blocklist,
                           params=self.params)

    async def image(self, query, pithumbsize=1000, **kwargs):
        return await ImageController(**self.params) \
                        .method(query, pithumbsize,
                                img_blocklist=self.img_blocklist, **kwargs)

    async def getPageName(self, id_):
        status, data = await self.driver.get(
            pageids=id_
        )

        try:
            return data.query.pages[-1].title
        except AttributeError:
            raise NotFound(f"Not found page with this id: {id_}")

    async def get_all(self, query, lurk=False,
                      blocklist=(), **kwargs):
        try:
            search = await self.search(query)

        except NotFound:
            await message.reply(_("errors.not_found"))
            return

        opensearch = await self.opensearch(
            query if lurk else search[0].title
        )

        if lurk:
            url = "example.com"
            page = await self.page(opensearch[0])

        else:
            url = opensearch[-1][0]
            page = await self.page(search[0])

        page.blockList = blocklist

        try:
            image = await page.image()
            image = image.source

        except Exception as e:
            print(e)
            image = -1

        return page, image, url
