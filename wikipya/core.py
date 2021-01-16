import requests
import json
import re

from bs4 import BeautifulSoup


class JSONObject:
    def __init__(self, dict):
        vars(self).update(dict)


class Wikipya:
    def __init__(self, lang):
        self.lang = lang
        self.url = f"https://{lang}.wikipedia.org/w/api.php"

    def _getLastItem(self, page):
        item = ""
        for tag in page:
            item = tag

        return item

    def _get(self, params):
        self.params = {"format": "json", "action": "query"}
        self.params = {**self.params, **params}

        r = requests.get(self.url, self.params)

        if not r.status_code == 200:
            return 404

        return json.loads(r.text, object_hook=JSONObject)

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

    def search(self, query, limit=1):
        data = self._get({
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "srprop": "size"
        })

        if len(data.query.search) == 0:
            return -1

        responce = data.query.search

        result = []

        for item in responce:
            # page = {"title": item["title"], "pageid": item["pageid"]}
            page = [item.title, item.pageid]
            result.append(page)

        return result

    def opensearch(self, query, limit=1):
        data = self._get({
                   "action": "opensearch",
                   "search": query,
                   "limit": 1
               })

        return data

    def getPageNameById(self, id_):
        data = self._get({"pageids": id_})

        try:
            return data.query.pages.__dict__[str(id_)].title
        except KeyError:
            return -1

    def getPage(self, title, exsentences=5):
        if exsentences == -1:
            data = self._get({
                "prop": "extracts",
                "titles": title
            })
        else:
            data = self._get({
                "prop": "extracts",
                "titles": title,
                "exsentences": exsentences
            })

        result = data.query.pages

        if "-1" in result.__dict__:
            return -1

        page_id = self._getLastItem(result.__dict__)

        print(result.__dict__[page_id].extract)

        return BeautifulSoup(result.__dict__[page_id].extract, "lxml")

    def getImageByPageName(self, title, pithumbsize=1000):
        data = self._get({
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

    def getImagesByPageName(self, title):
        return self._get({
            "prop": "pageimages",
            "piprop": "original",
            "titles": title
        })

    def parsePage(self, soup, title=""):
        for tag in soup.find_all("p"):
            if re.match(r"\s", tag.text):
                tag.replace_with("")

        for item in ["math", "semantics"]:
            for t in soup.findAll(item):
                t.replace_with("")

        if len(soup.find_all("p")) == 0:
            return soup.text
        else:
            p = soup.find_all("p")[0]

        bold_words = []

        for tag in p.find_all("b"):
            bold_words.append(tag.text)

        text = ""

        if p.text.find("означать:") != -1 or \
           p.text.find("refer to:") != -1 or \
           p.text.find("— многозначный термин, означающий:") != -1:
            text = self._prepare_list(soup)

        else:
            text = re.sub(r"\[.{,}\] ", "", p.text)

        for bold in bold_words:
            if text == f"{bold}:\n":
                text = self._prepare_list(soup)

        text = text.replace("<", "&lt;") \
                   .replace(">", "&gt;") \
                   .replace("  ", " ") \
                   .replace(" )", ")") \
                   .replace(" )", ")")

        for bold in bold_words:
            try:
                text = re.sub(bold, f"<b>{bold}</b>", text, 1)
            except re.error:
                text = text.replace(bold + " ", f"<b>{bold}</b> ")

        return text
