from test_common import CommonTestsWikipya

from wikipya.aiowiki import Wikipya


class TestWikipedia(CommonTestsWikipya):
    wikipya = Wikipya("ru", version="1.35", lurk=False)
