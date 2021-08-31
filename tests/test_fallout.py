from test_common import CommonTestsWikipyaLegacy

from wikipya.aiowiki import Wikipya
from wikipya.clients import MediaWiki_Legacy


class TestFallout(CommonTestsWikipyaLegacy):
    SEARCH_QUERY = "Марипоза"
    SEARCH_LIMIT = 1
    IMAGE_QUERY = "Стрип"

    wikipya = Wikipya(
        url="https://fallout.fandom.com/ru/api.php",
        # lurk=True,
        prefix="",
        # img_blocklist=blocklist["images"]
        client=MediaWiki_Legacy
    )
