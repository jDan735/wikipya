from pydantic import BaseModel, Field, RootModel
from typing import Optional

from .image import Image


class SearchResult(BaseModel):
    title: str
    snippet: Optional[str] = None
    size: Optional[int] = None
    page_id: Optional[int] = Field(None, alias="pageid")


class SearchResultWithDescripion(BaseModel):
    page_id: Optional[int] = Field(None, alias="pageid")
    title: str
    index: int
    thumbnail: Optional[Image] = None
    description: Optional[str] = None
    description_source: Optional[str] = Field(None, alias="descriptionsource")


Search = RootModel[list[SearchResult]]
SearchWithDescription = RootModel[list[SearchResultWithDescripion]]