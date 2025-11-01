import httpx

from typing import Any, Optional
from pydantic import BaseModel, Field

from .models import MediawikiUrl
from .constants import TAG_BLOCKLIST, DEFAULT_PARAMS
from .exceptions import ParseError


HEADERS: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Accept-Encoding": "gzip",
}


class BaseClient(BaseModel):
    url: MediawikiUrl
    timeout: Optional[int] = 5

    tag_blocklist: list[str] = Field(repr=False, default=TAG_BLOCKLIST)
    default_params: dict[str, str | int] = Field(repr=False, default=DEFAULT_PARAMS)

    client: Any | None = None

    def model_post_init(self, __context: Any) -> None:
        self.client = httpx.AsyncClient(timeout=self.timeout, headers=HEADERS)

    async def get(
        self, url: Optional[str] = None, **params: Any
    ) -> tuple[httpx.Response, Any]:
        res: httpx.Response = await self.client.get(
            str(url or self.url),
            params={**self.default_params, **params},
            follow_redirects=True,
        )

        json: Any = res.json()

        try:
            if error := json.get("error"):
                raise ParseError(f"{error['code']}: {error['info']}")
        except:  # noqa: E722
            pass

        return res, json

    async def get_html(self, url: Optional[str] = None, **params: Any):
        return await self.client.get(
            str(url or self.url), params=params, follow_redirects=True
        )


class MediaWiki(BaseClient):
    from .methods import (
        fetch_all,
        get_page_name,
        image,
        opensearch,
        page,
        search,
        sections,
        search_with_description,
    )


class Wikipedia(MediaWiki):
    from .methods import summary


class Fandom(MediaWiki):
    from .methods import (
        fandom_search,
        fandom_facade_search as search,
    )


class MediaWikiAbstract(BaseClient):
    from .methods import (
        fetch_all,
        get_page_name,
        image,
        opensearch,
        page,
        search,
        search as legacy_search,
        summary,
        sections,
        search_with_description,
        fandom_search,
    )
