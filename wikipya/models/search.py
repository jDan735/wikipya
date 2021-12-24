from pydantic import BaseModel, Field
from typing import Optional


class SearchResult(BaseModel):
    title: str
    snippet: Optional[str]
    size: Optional[int]
    page_id: Optional[int] = Field(alias="pageid")


class Search(BaseModel):
    __root__: list[SearchResult]
