import httpx

from typing import Any, Optional
from pydantic import BaseModel, Field

from .models import MediawikiUrl
from .constants import TAG_BLOCKLIST, DEFAULT_PARAMS
from .exceptions import ParseError


class BaseClient(BaseModel):
    url: MediawikiUrl
    timeout: Optional[int] = 5

    tag_blocklist: list[str] = Field(repr=False, default=TAG_BLOCKLIST)
    default_params: dict[str, str | int] = Field(repr=False, default=DEFAULT_PARAMS)

    async def get(
        self, url: Optional[str] = None, **params: Any
    ) -> tuple[httpx.Response, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            res: httpx.Response = await client.get(
                str(url or self.url),
                params={**self.default_params, **params},
                follow_redirects=True,
            )

        json: Any = res.json()

        try:
            if error := json.get("error"):
                raise ParseError(f'{error["code"]}: {error["info"]}')
        except:  # noqa: E722
            pass

        return res, json

    async def get_html(self, url: Optional[str] = None, **params: Any):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            return await client.get(
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
