from dataclasses import dataclass, field
from typing import Optional

from ..drivers import BaseDriver, HttpxDriver
from ..constants import DEFAULT_PARAMS, TAG_BLOCKLIST, IMAGE_BLOCKLIST


@dataclass
class BaseClient:
    url: str
    driver: BaseDriver = field(repr=False, default_factory=HttpxDriver)

    tag_blocklist: list = field(repr=False, default_factory=lambda: TAG_BLOCKLIST)
    img_blocklist: list = field(repr=False, default_factory=lambda: IMAGE_BLOCKLIST)

    default_params: dict = field(repr=False, default_factory=lambda: DEFAULT_PARAMS)

    def __post_init__(self):
        self.driver = self.driver(self.url, params=self.default_params)

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
