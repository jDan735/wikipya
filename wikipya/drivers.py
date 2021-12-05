try:
    import httpx
except ImportError:
    print("Not found httpx. Try pip install httpx")

from dataclasses import dataclass, field
from typing import Optional

from .exceptions import ParseError


@dataclass
class BaseDriver:
    url: str = "example.org"
    timeout: Optional[int] = 5
    params: dict = field(default_factory=dict)

    async def get(self, url, params=(), timeout=None):
        raise NotImplementedError


@dataclass
class HttpxDriver(BaseDriver):
    async def get(self, url=None, timeout=None, debug=False, **params):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            res = await client.get(str(url or self.url), params={**self.params, **params})

        res.json = res.json()

        if not isinstance(res.json, list) and (error := res.json.get("error")):
            raise ParseError(f'{error["code"]}: {error["info"]}')

        return res

    async def get_html(self, url=None, timeout=None, debug=False, **params):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            return await client.get(str(url or self.url), params=params, follow_redirects=True)
