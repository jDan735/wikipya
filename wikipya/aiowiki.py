import aiohttp
import json
import traceback

from bs4 import BeautifulSoup


class NotFound(Exception):
    def __init__(self, text):
        self.txt = text


class JSONObject:
    def __init__(self, dict):
        vars(self).update(dict)


class WikipyaPage:
    def __init__(self, html, query=None, title=None, pageid=None):
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

        self.html = html
        self.soup = BeautifulSoup(html, "lxml")

    def _pretty_list(self, list_):
        return list_.replace("0", "0️⃣") \
                    .replace("1", "1️⃣") \
                    .replace("2", "2️⃣") \
                    .replace("3", "3️⃣") \
                    .replace("4", "4️⃣") \
                    .replace("5", "5️⃣") \
                    .replace("6", "6️⃣") \
                    .replace("7", "7️⃣") \
                    .replace("8", "8️⃣") \
                    .replace("9", "9️⃣")

    def _prepare_list(self, text=""):
        for tag in self.soup.find_all("p"):
            text += tag.text

        text += "\n"

        for tag in self.soup.find_all("li"):
            ind = str(self.soup.find_all("li").index(tag) + 1)
            ind = self._pretty_list(ind)

            text += ind + " " + tag.text + "\n"

        return text

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
        data = await Wikipya._get({
            "titles": self.query.title,
            "prop": "pageimages",
            "pithumbsize": pithumbsize,
            "pilicense": "any",
        })

        image = data.query.pages

        try:
            return image.__dict__[self.pageid].thumbnail

        except AttributeError:
            raise NameError("Not found image")


class Wikipya:
    def __init__(self, lang):
        self.lang = lang
        self.url = f"https://{lang}.wikipedia.org/w/api.php"

    def _getLastItem(self, page, item=""):
        for tag in page:
            item = tag

        return item

    async def _get(self, params):
        self.params = {"format": "json", "action": "query"}
        self.params = {**self.params, **params}

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.params) as response:
                if not response.status == 200:
                    return 404

                text = await response.text()

                return json.loads(text, object_hook=JSONObject)

    async def search(self, query, limit=1):
        data = await self._get({"list": "search",
                                "srsearch": query,
                                "srlimit": limit,
                                "srprop": "size"})

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
        data = await self._get({
                   "action": "opensearch",
                   "search": query,
                   "limit": 1
               })

        if len(data) == 0:
            raise NotFound("OpenSearch can't find anything on your request")

        return data

    async def getPageName(self, id_):
        data = await self._get({"pageids": id_})

        try:
            return data["query"]["pages"][str(id_)]["title"]
        except KeyError:
            return -1

    async def page(self, query, exsentences=5):
        if exsentences == -1:
            exsentences_json = {}
        else:
            exsentences_json = {"exsentences": exsentences}

        data = await self._get({
            "prop": "extracts",
            "titles": query.title,
            **exsentences_json
        })

        result = data.query.pages

        if "-1" in result.__dict__:
            return -1

        id_ = self._getLastItem(result.__dict__)
        html = result.__dict__[id_].extract

        return WikipyaPage(html, query)
