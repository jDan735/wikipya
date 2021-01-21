import requests
import json
import re

import asyncio

from bs4 import BeautifulSoup

if __name__ == "__main__":
    from aiowiki import Wikipya as aiowiki, JSONObject
else:
    from .aiowiki import Wikipya as aiowiki, JSONObject


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
        return aiowiki._get(self, params)

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
        return asyncio.run(aiowiki.search(self, query, limit))

    def opensearch(self, query, limit=1):
        return asyncio.run(aiowiki.opensearch(self, query, limit))

    def getPageNameById(self, id_):
        return asyncio.run(aiowiki.getPageNameById(self, id_))

    def getPage(self, title, exsentences=5):
        return asyncio.run(aiowiki.getPage(self, title, exsentences))

    def getImageByPageName(self, title, pithumbsize=1000):
        return asyncio.run(aiowiki.getImageByPageName(self, title, pithumbsize))

    def getImagesByPageName(self, title):
        return asyncio.run(aiowiki.getImagesByPageName(self, title))

    def parsePage(self, soup, title=""):
        return aiowiki.parsePage(self, soup, title)

if __name__ == "__main__":
    w = Wikipya("ru")
    s = w.search("cmake")
    print(s)
    s = w.opensearch("cmake")
    p = w.getPage(s[1])
    print(w.parsePage(p))
    print(w.getImageByPageName("Украина"))
