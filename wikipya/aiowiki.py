from .drivers import AiohttpDriver
from .exceptions import NotFound

from .methods.search import Search
from .methods.opensearch import OpenSearch
from .methods.page import Page
from .methods.image import Image
from .methods.get_page_name import GetPageName


class Wikipya:
    def __init__(
        self, lang=None, driver=AiohttpDriver, version="1.35",
        url="https://{lang}.wikipedia.org/w/api.php", params={
            "format": "json",
            "action": "query",
            "formatversion": 2
        }
    ):
        """ Initialisation instance of Wikipya
        Args:
            lang: Lang of MediaWiki source
            driver: Driver for connection to service
            version: Version of MediaWiki
            url: Template of URL to wiki
            params: Default params for driver
        """

        self.MEDIAWIKI_VERSION = version

        self.lang = lang
        self.url = url if lang is None else url.format(
            lang=self.lang
        )

        self.driver = driver(url=self.url,
                             params=params)

    @property
    def params(self):
        return {
            "lang": self.lang,
            "driver": self.driver,
            "version": self.MEDIAWIKI_VERSION,
            "url": self.url
        }

    async def search(self, query, limit=1, **kwargs):
        return await Search(**self.params) \
            .method(query, limit, **kwargs)

    async def opensearch(self, query, limit=1, **kwargs):
        return await OpenSearch(**self.params) \
            .method(query, limit, **kwargs)

    async def page(self, query, section=0, **kwargs):
        return await Page(**self.params) \
            .method(query, section, **kwargs)

    async def _page(self, query, section=0, **kwargs):
        return await Page(**self.params) \
            ._page(query, section, **kwargs)

    async def image(self, query, pithumbsize=1000, **kwargs):
        return await Image(**self.params) \
            .method(query, pithumbsize, **kwargs)

    async def getPageName(self, id_):
        return await GetPageName(**self.params) \
            .method(id_)
