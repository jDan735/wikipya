from pydantic import BaseModel, Field
from typing import Optional

from .image import Image


class DesktopUrls(BaseModel):
    page: str


class ContentUrls(BaseModel):
    desktop: DesktopUrls


class Summary(BaseModel):
    title: str
    page_id: int = Field(alias="pageid")

    thumbnail: Optional[Image] = None
    original_image: Optional[Image] = Field(None, alias="originalimage")

    description: Optional[str] = None

    extract: str
    extract_html: str

    content_urls: ContentUrls
