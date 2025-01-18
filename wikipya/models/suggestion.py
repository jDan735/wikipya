from functools import cached_property
from typing import Optional
from pydantic import BaseModel, Field, RootModel, AliasChoices
from pydantic import HttpUrl


Redirect = RootModel[str]


def to_key(x: str) -> str:
    return x.title().replace(" ", "_")


class Suggestion(BaseModel):
    page_id: int = Field(validation_alias=AliasChoices("pageid", "page_id"))
    image: Optional[HttpUrl] = None

    key_: Optional[str] = Field(default=None, repr=None)  # type: ignore
    title: str

    description: Optional[str] = None

    @cached_property
    def key(self) -> str:
        if self.key_:
            return self.key_

        return to_key(self.title)


QuickSearchResults = RootModel[list[Suggestion]]
