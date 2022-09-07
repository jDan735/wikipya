from pydantic import BaseModel, Field
from typing import Optional

from .image import Image


class SearchResult(BaseModel):
    title: str
    snippet: Optional[str]
    size: Optional[int]
    page_id: Optional[int] = Field(alias="pageid")


class SearchResultWithDescripion(BaseModel):
    page_id: Optional[int] = Field(alias="pageid")
    title: str
    index: int
    thumbnail: Optional[Image]
    description: Optional[str]
    description_source: Optional[str] = Field(alias="descriptionsource")


class Search(BaseModel):
    __root__: list[SearchResult]


class SearchWithDescription(BaseModel):
    __root__: list[SearchResultWithDescripion]
