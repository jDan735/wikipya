from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    size: int


class Search(BaseModel):
    __root__: list[SearchResult]
