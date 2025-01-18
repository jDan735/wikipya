from pydantic.dataclasses import dataclass

from wikipya.clients import MediaWikiAbstract, Fandom, Wikipedia, MediaWiki


@dataclass
class Params:
    client: MediaWikiAbstract | Fandom | Wikipedia | MediaWiki

    allow_http: bool = False
    check_image_res: bool = True

    search_limit: int = 4
    search_query: str = "cmake"
    image_query: str = "Украина"
