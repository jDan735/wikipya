from .drivers import HttpxDriver
from .exceptions import NotFound

from .methods import ImageController
from .types import Image, SearchItem

from tghtml import TgHTML


WGR_FLAG = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb" +
    "/8/85/Flag_of_Belarus.svg/1000px-Flag_of_Belarus.svg.png"
)

WRW_FLAG = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb" +
    "/5/50/Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg" +
    "/1000px-Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg.png"
)


class Wikipya:
    def __init__(
        self, lang=None, Driver=HttpxDriver, version="1.0",
        url="https://{lang}.wikipedia.org/w/api.php", params={
            "format": "json",
            "action": "query",
            "formatversion": 2
        }, img_blocklist=(), host="", prefix="/w"
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
        self.prefix = prefix

        self.driver = Driver(url=self.url, params=params)

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
        search = await self.search(query)
        opensearch = await self.opensearch(
            query if lurk else search[0].title
        )

        if lurk:
            try:
                url, title = opensearch[-1][0], opensearch[1][0]
            except:
                url, title = None, search[0]
        else:
            url, title = opensearch[-1], search[0]

        page = await self.page(title)
        page.blockList = blocklist

        try:
            image = await page.image(prefix=self.prefix, debug=True)
            image = image.source

        except Exception as e:
            print(e)
            image = -1

        if image == WGR_FLAG:
            image = WRW_FLAG

        return page, image, url


class WikipyaPage:
    def __init__(self, parse, params, img_blocklist, lang="en"):
        vars(self).update(parse.__dict__)

        self.blockList = []
        self.lang = lang
        self.params = params      # fastfix for image
        self.img_blocklist = img_blocklist
        self.url = f"https://{lang}.wikipedia.org/w/api.php"

        # fix for lurkmore
        if self.text.__class__.__name__ == "JSONObject":
            self.text = self.text.__dict__["*"]

    @property
    def parsed(self):
        return str(TgHTML(self.text, self.blockList, is_wikipedia=False))

    @property
    def fixed(self):
        namelist = [
            ["Белоруссия", "Беларусь"],
            ["Белоруссии", "Беларуси"],
            ["Беларуссию", "Беларусь"],
            ["Белоруссией", "Беларусью"],
            ["Белоруссиею", "Беларусью"],

            ["Белору́ссия", "Белару́сь"],
            ["Белору́ссии", "Белару́си"],
            ["Белору́ссию", "Белару́сь"],
            ["Белору́ссией", "Белару́сью"],
            ["Белору́ссиею", "Белару́сью"],


            ["на Украин", "в Украин"],
        ]

        for name in namelist:
            text = self.parsed.replace(*name)

        return text

    async def image(self, pithumbsize=1000, **kwargs):
        return await ImageController(**self.params) \
            .method(self.title, pithumbsize, img_blocklist=self.img_blocklist, **kwargs)
