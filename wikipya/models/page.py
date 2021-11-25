from pydantic import BaseModel
from tghtml import TgHTML

from typing import Optional


class Redirect(BaseModel):
    pass


class Page(BaseModel):
    title: str
    redirects: list[Redirect]
    text: str

    tag_blocklist: Optional[list]

    @property
    def parsed(self):
        return str(TgHTML(self.text, self.tag_blocklist, is_wikipedia=False))
