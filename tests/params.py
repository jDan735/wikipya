from dataclasses import dataclass

from wikipya import Wikipya


@dataclass
class Params:
    client: Wikipya

    allow_http: bool = False
    check_image_res: bool = True

    search_limit: int = 4
    search_query: str = "cmake"
    image_query: str = "Украина"
