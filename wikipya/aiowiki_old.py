import aiohttp
import json

from tghtml import TgHTML as tghtml


class NotFound(Exception):
    def __init__(self, text):
        self.txt = text


class JSONObject:
    """JSON => Class"""
    def __init__(self, dict):
        self.add(dict)

    def add(self, dict):
        self._dict = dict
        vars(self).update(dict)


class SearchItem:
    def __init__(self, title, pageid):
        self.title = title
        self.pageid = pageid


class WikipyaPage:
    def __init__(self, parse, lang="en"):
        vars(self).update(parse._dict)

        self.blockList = []
        self.lang = lang
        self.url = f"https://{lang}.wikipedia.org/w/api.php"

    @property
    def parsed(self):
        return tghtml(self.text, self.blockList)

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

    async def image(self, pithumbsize=1000):
        """ Get page image

        Example url:
            api.php?action=query&titles=Ukraine&prop=pageimages&pithumbsize=1000&pilicense=any&format=json
        """

        data = await Wikipya._get(self, titles=self.title,
                                  prop="pageimages", pilicense="any",
                                  pithumbsize=pithumbsize)

        try:
            image = data.query.pages[-1]
            thumb = image.thumbnail

            return JSONObject({
                "source": thumb.source,
                "width": thumb.width,
                "height": thumb.height
            })

        except AttributeError:
            raise NotFound("Not found image")


class Wikipya:
    def __init__(self, lang):
        self.lang = lang
        self.url = f"https://{lang}.wikipedia.org/w/api.php"

    async def _get(self, **kwargs):
        self.params = {"format": "json", "action": "query",
                       "formatversion": 2}
        self.params = {**self.params, **kwargs}

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.params) as response:
                print(response.url)
                if not response.status == 200:
                    return 404

                text = await response.text()

                return json.loads(text, object_hook=JSONObject)

    async def search(self, query, limit=1, prop="size"):
        data = await self._get(list="search", srsearch=query,
                               srlimit=limit, srprop=prop)

        if len(data.query.search) == 0:
            raise NotFound("Search can't find anything on your request")

        responce = data.query.search

        result = []

        for item in responce:
            result.append(SearchItem(title=item.title, pageid=item.pageid))

        return result

    async def opensearch(self, query, limit=1):
        data = await self._get(action="opensearch", search=query, limit=limit)

        if len(data) == 0:
            raise NotFound("OpenSearch can't find anything on your request")

        return data

    async def getPageName(self, id_):
        data = await self._get(pageids=id_)

        try:
            return data.query.pages[-1].title
        except AttributeError:
            raise NotFound(f"Not found page with this id: {id_}")

    async def _page(self, query, exsentences=5):
        if exsentences == -1:
            exsentences_json = {}
        else:
            exsentences_json = {"exsentences": exsentences}

        data = await self._get(prop="extracts", titles=query.title,
                               formatversion=1, **exsentences_json)

        result = data.query.pages.__dict__

        if "-1" in result:
            return -1

        query = result[list(result.keys())[-1]]
        query.add({"text": query.extract})

        return WikipyaPage(query, lang=self.lang)

    async def page(self, query, prop="text", section=0):
        """ Get pages html code

        Example url:
            api.php?action=parse&page=Pet&prop=text&formatversion=2
        """

        if query.__class__ == str:
            params = {"page": query}

        elif query.__class__ == int:
            params = {"pageid": query}

        elif query.__class__ == SearchItem:
            params = {"pageid": query.pageid}

        data = await self._get(action="parse", section=section, prop=prop, **params)

        return WikipyaPage(data.parse, lang=self.lang)
