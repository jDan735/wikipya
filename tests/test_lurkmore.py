from test_common import CommonTestsWikipyaLegacy

from wikipya.aiowiki import Wikipya
from wikipya.clients.mediawiki_lurk import MediaWiki_Lurk


class TestLurkmore(CommonTestsWikipyaLegacy):
    SEARCH_QUERY = "эта страна"
    SEARCH_LIMIT = 1
    IMAGE_QUERY = "Украина"

    wikipya = Wikipya(
        url="https://ipv6.lurkmo.re/api.php",
        # lurk=True,
        prefix="",
        # img_blocklist=blocklist["images"]
        lurk=True
    )
