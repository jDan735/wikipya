from msgspec import Struct

from wikipya.clients import MediaWikiAbstract, Fandom, Wikipedia, MediaWiki
from wikipya import Wikipya

DEFAULT_WIKIPYA_PARAMS = dict(
    automatic_session_open=False,
    automatic_session_close=False,
)


class Params(Struct, frozen=True):
    allow_http: bool = False
    check_image_res: bool = True

    search_limit: int = 4
    search_query: str = "cmake"
    image_query: str = "Украина"


clients = (
    (Wikipya("ru", params=DEFAULT_WIKIPYA_PARAMS), Params()),
    (
        Wikipya(
            base_url="https://fallout.fandom.com/ru/api.php",
            prefix="",
            params=DEFAULT_WIKIPYA_PARAMS,
        ),
        Params(
            search_query="Марипоза",
            search_limit=1,
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
            search_limit=1,
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
            search_limit=1,
        ),
    ),
)
