import pytest
from wikipya import Wikipya
from wikipya.clients.mediawiki_legacy import MediaWiki_Legacy
from pytest_lazyfixture import lazy_fixture

from params import Params


@pytest.fixture(params=[
    lazy_fixture("lurkmore"),
    lazy_fixture("wikipedia"),
    lazy_fixture("fallout"),
    lazy_fixture("kaiserreich")
])
def params(request):
    return request.param


@pytest.fixture(scope="class")
def lurkmore():
    """Went lurkmore instance"""

    return Params(
        client=Wikipya(
            url="https://ipv6.lurkmo.re/api.php",
            prefix="",
            # img_blocklist=blocklist["images"]
        ),

        search_limit=1,
        search_query="эта страна",
        image_query="Украина"
    )


@pytest.fixture(scope="class")
def wikipedia():
    """Went wikipedia instance"""

    return Params(
        client=Wikipya("ru", version="1.35", lurk=False),
    )


@pytest.fixture(scope="class")
def fallout():
    """Went fallout instance"""

    return Params(
        client=Wikipya(
            url="https://fallout.fandom.com/ru/api.php",
            prefix="",
            client=MediaWiki_Legacy
        ),
        search_query="Марипоза",
        search_limit=1,
        image_query="Стрип"
    )


@pytest.fixture(scope="class")
def kaiserreich():
    """Went kaiserreich instance"""

    return Params(
        client=Wikipya(
            url="https://kaiserreich.fandom.com/ru/api.php",
            prefix="",
            client=MediaWiki_Legacy
        ),
        search_query="Германская империя",
        search_limit=1
    )
