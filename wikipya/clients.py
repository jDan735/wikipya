from dataclasses import dataclass, field

from .drivers import BaseDriver, HttpxDriver
from .constants import TAG_BLOCKLIST, IMAGE_BLOCKLIST, DEFAULT_PARAMS


@dataclass
class BaseClient:
    url: str
    driver: BaseDriver = field(repr=False, default_factory=HttpxDriver)

    tag_blocklist: list = field(repr=False, default_factory=lambda: TAG_BLOCKLIST)
    img_blocklist: list = field(repr=False, default_factory=lambda: IMAGE_BLOCKLIST)

    default_params: dict = field(repr=False, default_factory=lambda: DEFAULT_PARAMS)

    def __post_init__(self):
        self.driver = self.driver(self.url, params=self.default_params)


@dataclass
class MediaWiki(BaseClient):
    from .methods import (
        get_all,
        get_page_name,
        image,
        opensearch,
        page,
        search,
        summary,
        sections
    )


@dataclass
class MediaWiki_Legacy(MediaWiki):
    from .methods import get_images_list, get_image, legacy_image as image


@dataclass
class MediaWiki_Lurk(MediaWiki_Legacy):
    pass
