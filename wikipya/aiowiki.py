from .clients import *
from .drivers import HttpxDriver

from .exceptions import NotFound


class Wikipya:
    def __init__(
        self,
        lang=None,
        url="https://{lang}.wikipedia.org/w/api.php",
        params={
            "format": "json",
            "action": "query",
            "formatversion": 2
        },
        host="",
        prefix="/w",
        client=MediaWiki,
        version=None,  # unsupported,
        lurk=True,
        **kwargs
    ):
        self.url = url.format(lang=lang)
        self.prefix = prefix

        client = MediaWiki_Lurk if lurk else client
        client = client(HttpxDriver, self.url)

        methods = [func for func in dir(BaseClient)
                   if callable(getattr(BaseClient, func)) and
                   not func.startswith("__")]

        for method in methods:
            setattr(self, method, getattr(client, method))
