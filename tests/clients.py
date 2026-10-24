from msgspec import Struct

from wikipya.clients import MediaWikiAbstract, Fandom, Wikipedia, MediaWiki
from wikipya import Wikipya

DEFAULT_WIKIPYA_PARAMS = dict(
    automatic_session_open=False,
    automatic_session_close=False,
)


class Params(Struct, frozen=True, kw_only=True):
    allow_http: bool = False
    check_image_res: bool = True

    search_limit: int = 1
    search_query: str
    search_query_id: int
    image_query: str


clients = (
    (
        Wikipya(
            "ru",
            params=DEFAULT_WIKIPYA_PARAMS
        ),
        Params(
            search_query="cmake",
            search_query_id=1482272,
            search_limit=4,
            image_query="Украина"
        )
    ),
    (
        Wikipya(
            base_url="https://fallout.fandom.com/ru/api.php",
            prefix="",
            params=DEFAULT_WIKIPYA_PARAMS,
        ),
        Params(
            search_query="Марипоза",
            search_query_id=1787,
            image_query="Стрип",
        ),
    ),
    (
        Wikipya(
            base_url="https://buckshot-roulette.fandom.com/api.php",
            prefix="",
            params=DEFAULT_WIKIPYA_PARAMS,
        ),
        Params(
            search_query="Expired Medicine",
            search_query_id=247,
            image_query="Expired Medicine",
        ),
    ),
    (
        Wikipya(
            base_url="https://kaiserreich.fandom.com/ru/api.php",
            prefix="",
            params=DEFAULT_WIKIPYA_PARAMS,
        ),
        Params(
            search_query="Германская империя",
            search_query_id=147,
            image_query="Германская империя"
        ),
    ),
)
