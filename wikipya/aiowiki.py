import aiohttp
import json
import re

from bs4 import BeautifulSoup


class Wikipya:
    def __init__(self, lang):
        self.lang = lang
        self.url = f"https://{lang}.wikipedia.org/w/api.php"

    def _getLastItem(self, page):
        item = ""
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

                return json.loads(await response.text())

    async def search(self, query, limit=1):
        data = await self._get({"list": "search",
                                "srsearch": query,
                                "srlimit": limit,
                                "srprop": "size"
                                })

        if len(data["query"]["search"]) == 0:
            return -1

        responce = data["query"]["search"]

        result = []

        for item in responce:
            # page = {"title": item["title"], "pageid": item["pageid"]}
            page = [item["title"], item["pageid"]]
            result.append(page)

        return result

    def getPageNameById(self, id_):
        data = self._get({"pageids": id_})

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

        result = data["query"]["pages"]

        if "-1" in result:
            return -1

        page_html = result[self._getLastItem(result)]["extract"]
        soup = BeautifulSoup(page_html, "lxml")

        return soup

    async def getImageByPageName(self, title, pithumbsize=1000):
        data = await self._get({
            "titles": title,
            "prop": "pageimages",
            "pithumbsize": pithumbsize,
            "pilicense": "any",
        })

        image_info = data["query"]["pages"]
        pageid = self._getLastItem(image_info)

        try:
            return image_info[pageid]["thumbnail"]

        except KeyError:
            return -1

    async def getImagesByPageName(self, title):
        return await self._get({
            "prop": "pageimages",
            "piprop": "original",
            "titles": title
        })

    def parsePage(self, soup, title=""):
        for tag in soup.find_all("p"):
            if re.match(r"\s", tag.text):
                tag.replace_with("")

        for t in soup.findAll("math"):
            t.replace_with("")

        for t in soup.findAll("semantics"):
            t.replace_with("")

        if len(soup.find_all("p")) == 0:
            return "Беды с башкой 102"
        else:
            p = soup.find_all("p")[0]

        bold_text = []

        for tag in p.find_all("b"):
            bold_text.append(tag.text)

        text = ""

        if p.text.find("означать:") != -1 or \
           p.text.find(f"{title}:") != -1 or \
           p.text.find("— многозначный термин, означающий:") != -1:
            for tag in soup.find_all("p"):
                text += tag.text

            text += "\n"

            for tag in soup.find_all("li"):
                ind = str(soup.find_all("li").index(tag) + 1)

                ind = ind.replace("0", "0️⃣") \
                         .replace("1", "1️⃣") \
                         .replace("2", "2️⃣") \
                         .replace("3", "3️⃣") \
                         .replace("4", "4️⃣") \
                         .replace("5", "5️⃣") \
                         .replace("6", "6️⃣") \
                         .replace("7", "7️⃣") \
                         .replace("8", "8️⃣") \
                         .replace("9", "9️⃣")

                text += ind + " " + tag.text + "\n"

        else:
            text = re.sub(r"\[.{,}\] ", "", p.text)

        for bold in bold_text:
            if text == f"{bold}:\n":
                text = ""
                for tag in soup.find_all("p"):
                    text += tag.text

                text += "\n"

                for tag in soup.find_all("li"):
                    ind = str(soup.find_all("li").index(tag) + 1)

                    ind = ind.replace("0", "0️⃣") \
                             .replace("1", "1️⃣") \
                             .replace("2", "2️⃣") \
                             .replace("3", "3️⃣") \
                             .replace("4", "4️⃣") \
                             .replace("5", "5️⃣") \
                             .replace("6", "6️⃣") \
                             .replace("7", "7️⃣") \
                             .replace("8", "8️⃣") \
                             .replace("9", "9️⃣")

                    text += ind + " " + tag.text + "\n"

        if text == "":
            return "Беды с башкой 168"

        text = text.replace("<", "&lt;") \
                   .replace(">", "&gt;") \
                   .replace("  ", " ") \
                   .replace(" )", ")") \
                   .replace(" )", ")")

        for bold in bold_text:
            try:
                text = re.sub(bold, f"<b>{bold}</b>", text, 1)
            except re.error:
                text = text.replace(bold + " ", f"<b>{bold}</b> ")

        return text
