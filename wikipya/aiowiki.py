import aiohttp
import json
import traceback

from bs4 import BeautifulSoup


class JSONObject:
    def __init__(self, dict):
        vars(self).update(dict)


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

                return json.loads(await response.text(),
                                  object_hook=JSONObject)

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

    def _prepare_list(self, soup, text=""):
        for tag in soup.find_all("p"):
            text += tag.text

        text += "\n"

        for tag in soup.find_all("li"):
            ind = str(soup.find_all("li").index(tag) + 1)
            ind = self._pretty_list(ind)

            text += ind + " " + tag.text + "\n"

        return text

    async def search(self, query, limit=1):
        data = await self._get({"list": "search",
                                "srsearch": query,
                                "srlimit": limit,
                                "srprop": "size"
                                })

        if len(data.query.search) == 0:
            return -1

        responce = data.query.search

        result = []

        for item in responce:
            page = [item.title, item.pageid]
            result.append(page)

        return result

    async def opensearch(self, query, limit=1):
        data = await self._get({
                   "action": "opensearch",
                   "search": query,
                   "limit": 1
               })

        return data

    async def getPageNameById(self, id_):
        data = await self._get({"pageids": id_})

        try:
            return data["query"]["pages"][str(id_)]["title"]
        except KeyError:
            return -1

    async def getPage(self, title, exsentences=5):
        if exsentences == -1:
            data = await self._get({
                "prop": "extracts",
                "titles": title
            })
        else:
            data = await self._get({
                "prop": "extracts",
                "titles": title,
                "exsentences": exsentences
            })

        result = data.query.pages

        if "-1" in result.__dict__:
            return -1

        page_id = self._getLastItem(result.__dict__)
        page_html = result.__dict__[page_id].extract

        return BeautifulSoup(page_html, "lxml")

    async def getImageByPageName(self, title, pithumbsize=1000):
        data = await self._get({
            "titles": title,
            "prop": "pageimages",
            "pithumbsize": pithumbsize,
            "pilicense": "any",
        })

        image_info = data.query.pages
        pageid = self._getLastItem(image_info.__dict__)

        try:
            return image_info.__dict__[pageid].thumbnail

        except AttributeError:
            return -1

    async def getImagesByPageName(self, title):
        return await self._get({
            "prop": "pageimages",
            "piprop": "original",
            "titles": title
        })

    def parsePage(self, soup, title=""):
        try:
            for t in soup.findAll("p"):
                if "Это статья об" in t.text:
                    t.replace_with("")

            tagBlocklist = [["math"], ["semantics"]]

            for item in tagBlocklist:
                for tag in soup.findAll(*item):
                    try:
                        tag.replace_with("")
                    except Exception:
                        pass

            for tag in soup.findAll("p"):
                if tag.text.replace("\n", "") == "":
                    tag.replace_with("")
        except Exception:
            print(traceback.format_exc())

        try:
            soup = soup.p
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
