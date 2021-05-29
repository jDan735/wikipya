import aiohttp
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
    async def get(self, url=None, timeout=None, **params):
        params = {**self.params, **params}

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url or self.url, params=params,
                timeout=timeout or self.timeout
            ) as response:
                text = await response.text()

                try:
                    return response.status, json.loads(
                        text, object_hook=JSONObject
                    )
                except Exception as e:
                    print(e)
                    return response.status, text
