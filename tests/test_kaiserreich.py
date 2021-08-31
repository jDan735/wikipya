from test_common import CommonTestsWikipyaLegacy

from wikipya.aiowiki import Wikipya
from wikipya.clients import MediaWiki_Legacy


class TestKaiserreich(CommonTestsWikipyaLegacy):
    SEARCH_QUERY = "Германская империя"
    SEARCH_LIMIT = 1

    wikipya = Wikipya(
        url="https://kaiserreich.fandom.com/ru/api.php",
        # lurk=True,
        prefix="",
        # img_blocklist=blocklist["images"]
        client=MediaWiki_Legacy
    )
