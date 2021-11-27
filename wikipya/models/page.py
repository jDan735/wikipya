from pydantic import BaseModel, Field
from tghtml import TgHTML

from typing import Optional


class Page(BaseModel):
    title: str
    text: str

    tag_blocklist: Optional[list] = Field(repr=False)

    @property
    def parsed(self):
        return TgHTML(self.text, self.tag_blocklist).parsed

    @property
    def fixed(self):
        print("Page.fixed is deprecated, please use .parsed!")
        return self.parsed
