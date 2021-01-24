import traceback
import aiohttp
import json

from bs4 import BeautifulSoup


class NotFound(Exception):
    def __init__(self, text):
        self.txt = text


class JSONObject:
    """JSON => Class"""
    def __init__(self, dict):
        vars(self).update(dict)


class WikipyaPage:
    def __init__(self, html, query=None, title=None, pageid=None, lang="en"):
        if query is None:
            if title is not None and pageid is not None:
                self.query = JSONObject({
                    "title": title,
                    "pageid": pageid
                })
            else:
                raise NameError("query or pageid & name is not defined")
        else:
            self.query = query

        self.pageid = self.query.pageid
        self.title = self.query.title

        self.lang = lang
        self.url = f"https://{lang}.wikipedia.org/w/api.php"
        self.html = html
        self.soup = BeautifulSoup(html, "lxml")

    def parse(self):
        """This function went html parsed to tghtml"""

        try:
            for t in self.soup.findAll("p"):
                if "Это статья об" in t.text:
                    t.replace_with("")

            tagBlocklist = [["math"], ["semantics"]]

            for item in tagBlocklist:
                for tag in self.soup.findAll(*item):
                    try:
                        tag.replace_with("")
                    except Exception:
                        pass

            for tag in self.soup.findAll("p"):
                if tag.text.replace("\n", "") == "":
                    tag.replace_with("")
        except Exception:
            print(traceback.format_exc())

        try:
            soup = self.soup.p
            for tag in soup():
                for attribute in ["class", "title", "href", "style", "name",
                                  "id", "dir", "lang", "rel"]:
                    try:
                        del tag[attribute]
                    except Exception:
                        pass

            return str(soup).replace("<p>", "") \
                            .replace("<a>", "") \
                            .replace("<span>", "") \
                            .replace("</p>", "") \
                            .replace("</a>", "") \
                            .replace("</span>", "")

        except Exception as e:
            print(e)
            return "Не удалось распарсить"

    async def image(self, pithumbsize=1000):
        """ Get page image

        Example url:
            api.php?action=query&titles=Ukraine&prop=pageimages&pithumbsize=1000&pilicense=any&format=json
        """

        data = await Wikipya._get(self, titles=self.query.title,
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

    def _getLastItem(self, page, item=""):
        for tag in page:
            item = tag

        return item

    async def _get(self, **kwargs):
        self.params = {"format": "json", "action": "query",
                       "formatversion": 2}
        self.params = {**self.params, **kwargs}

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.params) as response:
                if not response.status == 200:
                    return 404

                text = await response.text()

                return json.loads(text, object_hook=JSONObject)

    async def search(self, query, limit=1):
        data = await self._get(list="search", srsearch=query,
                               srlimit=limit, srprop="size")

        if len(data.query.search) == 0:
            raise NotFound("Search can't find anything on your request")

        responce = data.query.search

        result = []

        for item in responce:
            result.append(JSONObject({
                "title": item.title,
                "pageid": item.pageid
            }))

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

        result = data.query.pages

        if "-1" in result.__dict__:
            return -1

        id_ = self._getLastItem(result.__dict__)
        html = result.__dict__[id_].extract

        return WikipyaPage(html, query, lang=self.lang)

    async def page(self, query, section=0):
        """ Get pages html code

        Example url:
            api.php?action=parse&page=Pet&prop=text&formatversion=2
        """

        data = await self._get(action="parse", pageid=query.pageid,
                               section=section)

        html = data.parse.text

        return WikipyaPage(html, query, lang=self.lang)
