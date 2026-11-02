from msgspec import Struct, field
from typing import Optional


class Image(Struct, frozen=True):
    source: str
    width: Optional[int] = None
    height: Optional[int] = None


class DesktopUrls(Struct, frozen=True):
    page: str


class ContentUrls(Struct, frozen=True):
    desktop: DesktopUrls


class Summary(Struct, frozen=True, kw_only=True):
    title: str
    page_id: int = field(name="pageid")

    thumbnail: Optional[Image] = None
    original_image: Optional[Image] = field(
        default=None,
        name="originalimage",
    )

    description: Optional[str] = None

    extract: str
    extract_html: str

    content_urls: ContentUrls
