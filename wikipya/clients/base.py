from dataclasses import dataclass, field

from ..drivers import BaseDriver, HttpxDriver


@dataclass
class BaseClient:
    url: str
    prefix: str
    driver: BaseDriver = field(repr=False, default_factory=HttpxDriver)

    img_blocklist: list = field(default_factory=list, repr=False)

    DEFAULT_PARAMS = {
        "format": "json",
        "action": "query",
        "formatversion": 2
    }

    def __post_init__(self):
        self.driver = self.driver(self.url, params=self.DEFAULT_PARAMS)

    async def search(self, *args, **kwargs):
        raise NotImplementedError

    async def opensearch(self, *args, **kwargs):
        raise NotImplementedError

    async def page(self, *args, **kwargs):
        raise NotImplementedError

    async def _page(self, *args, **kwargs):
        raise NotImplementedError

    async def image(self, *args, **kwargs):
        raise NotImplementedError

    async def get_all(self, *args, **kwargs):
        raise NotImplementedError

    async def get_page_name(self, *args, **kwargs):
        raise NotImplementedError
