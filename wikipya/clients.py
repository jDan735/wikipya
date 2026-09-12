try:
    import httpx

    http_client = "httpx"
except ModuleNotFoundError:
    import aiohttp

    http_client = "aiohttp"

from typing import Any, Optional
from pydantic import BaseModel, Field

from .models import MediawikiUrl
from .constants import TAG_BLOCKLIST, DEFAULT_PARAMS
from .exceptions import ParseError

from msgspec import json

HEADERS: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Accept-Encoding": "gzip",
}


class HttpxClient(BaseModel):
    url: MediawikiUrl
    timeout: Optional[int] = 5

    tag_blocklist: list[str] = Field(repr=False, default=TAG_BLOCKLIST)
    default_params: dict[str, str | int] = Field(repr=False, default=DEFAULT_PARAMS)

    client: Any | None = None
    automatic_session_open: bool = True
    automatic_session_close: bool = True

    def model_post_init(self, __context: Any) -> None:
        if self.automatic_session_open:
            self.open()

    def open(self) -> None:
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            headers=HEADERS,
            http2=True,
        )

    async def get(
        self, url: Optional[str] = None, **params: Any
    ) -> tuple[httpx.Response, Any]:
        res: httpx.Response = await self.client.get(
            str(url or self.url),
            params={**self.default_params, **params},
            follow_redirects=True,
        )

        _: Any = json.decode(res.text)

        try:
            if error := _.get("error"):
                raise ParseError(f"{error['code']}: {error['info']}")
        except:  # noqa: E722
            pass

        return res, _

    async def close(self):...

    async def get_html(self, url: Optional[str] = None, **params: Any):
        return await self.client.get(
            str(url or self.url), params=params, follow_redirects=True
        )


class AiohttpClient(BaseModel):
    url: MediawikiUrl
    timeout: Optional[int] = 5

    tag_blocklist: list[str] = Field(repr=False, default=TAG_BLOCKLIST)
    default_params: dict[str, str | int] = Field(repr=False, default=DEFAULT_PARAMS)

    session: Optional[Any] = None
    automatic_session_open: bool = True
    automatic_session_close: bool = True

    def model_post_init(self, __context: Any) -> None:
        if self.automatic_session_open:
            self.open()

    def open(self) -> None:
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(self.timeout),
            headers=HEADERS,
        )

    async def get(
        self, url: Optional[str] = None, close_me: bool=True, **params: Any
    ) -> tuple[aiohttp.Response, Any]:
        res: aiohttp.Response = await self.session.get(
            str(url or self.url),
            params={**self.default_params, **params},
            allow_redirects=True,
        )

        _: Any = json.decode(await res.text())

        if self.automatic_session_close:
            await self.session.close()

        try:
            if error := _.get("error"):
                raise ParseError(f"{error['code']}: {error['info']}")
        except:  # noqa: E722
            pass

        return res, _

    async def close(self):
        await self.session.close()

    async def get_html(
        self, url: Optional[str] = None, close_me: bool=True, **params: Any
    ) -> tuple[aiohttp.Response, Any]:
        res: aiohttp.Response = await self.session.get(
            str(url or self.url),
            params={**self.default_params, **params},
            allow_redirects=True,
        )

        _: Any = await res.text()

        if self.automatic_session_close:
            await self.session.close()

        return res, _


class BaseClient(HttpxClient if http_client == "httpx" else AiohttpClient): ...


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
    from .methods import rest_search


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
