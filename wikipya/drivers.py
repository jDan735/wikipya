try:
    import aiohttp
except:
    pass

try:
    import httpx
except:
    pass

import time
import json

from .exceptions import ParseError


class JSONObject:
    """JSON => Class"""
    def __init__(self, dict):
        self.add(dict)

    def add(self, dict):
        vars(self).update(dict)


class BaseDriver:
    def __init__(self, url="example.com", timeout=5, params=()):
        self.timeout = timeout
        self.params = params
        self.url = url

    async def get(self, url, params=(), timeout=None):
        raise NotImplementedError


class AiohttpDriver(BaseDriver):
    async def get(self, url=None, timeout=None, debug=False, **params):
        if len(list(params.keys())) == 0:
            params = None
        else:
            params = {**self.params, **params}

        async with aiohttp.ClientSession() as session:
            start = time.time()

            async with session.get(
                url or self.url, params=params,
                timeout=timeout or self.timeout
            ) as response:
                text = await response.text()

                if debug:
                    print(response.url)
                    print(time.time() - start)

                js = json.loads(text, object_hook=JSONObject)

                if isinstance(js, list):
                    pass

                elif js.__dict__.get("error") is not None:
                    raise ParseError(f"{js.error.code}: {js.error.info}")

                return response.status, js

    async def get_html(self, url=None, timeout=None, debug=False, **params):
        if len(list(params.keys())) == 0:
            params = None
        else:
            params = {**self.params, **params}

        async with aiohttp.ClientSession() as session:
            start = time.time()

            async with session.get(
                url or self.url, params=params,
                timeout=timeout or self.timeout
            ) as response:
                text = await response.text()

                if debug:
                    print(response.url)
                    print(time.time() - start)

                return response.status, text, response.url


class HttpxDriver(BaseDriver):
    async def get(self, url=None, timeout=None, debug=False, **params):
        if len(list(params.keys())) == 0:
            params = None
        else:
            params = {**self.params, **params}

        async with httpx.AsyncClient() as client:
            start = time.time()

            res = await client.get(url or self.url, params=params,
                                   timeout=timeout or self.timeout)

            if debug:
                print(res.url)
                print(time.time() - start)

            js = json.loads(res.text, object_hook=JSONObject)

            if isinstance(js, list):
                pass
            elif js.__dict__.get("error"):
                raise ParseError(f"{js.error.code}: {js.error.info}")

            return res.status_code, js

    async def get_html(self, url=None, timeout=None, debug=False, **params):
        if len(list(params.keys())) == 0:
            params = None
        else:
            params = {**self.params, **params}

        async with httpx.AsyncClient() as client:
            start = time.time()

            res = await client.get(url or self.url, params=params,
                                   timeout=timeout or self.timeout)

            if debug:
                print(res.url)
                print(time.time() - start)

            return res.status_code, res.text, res.url
