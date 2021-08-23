from .mediawiki_legacy import MediaWiki_Legacy
from ..types import SearchItem, WikipyaPage, Image
from ..exceptions import NotFound


class MediaWiki_Lurk(MediaWiki_Legacy):
    DEFAULT_PARAMS = {
        "format": "json",
        "action": "query",
        "formatversion": 2
    }

    LANG = None
