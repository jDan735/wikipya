import pytest
from wikipya import Wikipya
from pytest_lazyfixture import lazy_fixture

from params import Params


@pytest.fixture(
    params=[
        lazy_fixture("buckshot"),
        lazy_fixture("wikipedia"),
        lazy_fixture("fallout"),
        lazy_fixture("kaiserreich"),
    ]
)
def params(request):
    return request.param


@pytest.fixture(scope="class")
def lurkmore():
    """Went lurkmore instance"""

    return Params(
        client=Wikipya(base_url="https://ipv6.lurkmo.re/api.php", prefix=""),
        search_limit=1,
        search_query="эта страна",
        image_query="Украина",
    )


@pytest.fixture(scope="class")
def wikipedia():
    """Went wikipedia instance"""

    return Params(
        client=Wikipya("ru"),
    )


@pytest.fixture(scope="class")
def fallout():
    """Went fallout instance"""

    return Params(
        client=Wikipya(base_url="https://fallout.fandom.com/ru/api.php", prefix=""),
        search_query="Марипоза",
        search_limit=1,
        image_query="Стрип",
    )


@pytest.fixture(scope="class")
def buckshot():
    """Went buckshot instance"""

    return Params(
        client=Wikipya(
            base_url="https://buckshot-roulette.fandom.com/api.php",
            prefix="",
        ),
        search_query="Expired Medicine",
        search_limit=1,
        image_query="Expired Medicine",
    )


@pytest.fixture(scope="class")
def kaiserreich():
    """Went kaiserreich instance"""

    return Params(
        client=Wikipya(
            base_url="https://kaiserreich.fandom.com/ru/api.php",
            prefix="",
        ),
        search_query="Германская империя",
        search_limit=1,
    )
