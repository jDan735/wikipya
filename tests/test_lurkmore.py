from test_common import CommonTestsWikipyaLegacy

from wikipya.aiowiki import Wikipya
from wikipya.clients import MediaWiki_Lurk


class TestLurkmore(CommonTestsWikipyaLegacy):
    SEARCH_QUERY = "эта страна"
    SEARCH_LIMIT = 1
    IMAGE_QUERY = "Украина"
    ALLOW_HTTP = True  # Now not work with https 

    wikipya = Wikipya(
        url="http://lurkmore.to/api.php",
        # lurk=True,
        prefix="",
        # img_blocklist=blocklist["images"]
        lurk=True
    )
