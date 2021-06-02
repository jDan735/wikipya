import aiohttp

import time
import json


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

                return response.status, json.loads(
                    text, object_hook=JSONObject
                )

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
