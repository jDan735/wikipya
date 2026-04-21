from typing import Optional

from pydantic import BaseModel, Field
from tghtml import TgHTML

from .section import Section


class Page(BaseModel):
    title: str
    pageid: Optional[int] = None

    text: Optional[str]
    sections: Optional[list[Section]] = None

    tag_blocklist: Optional[list] = Field(None, repr=False)

    @property
    def parsed(self):
        if (html := TgHTML(self.text, self.tag_blocklist or []).parsed) == "":
            html = TgHTML(self.text, self.tag_blocklist, enable_preprocess=False).parsed

        return html

    @property
    def fixed(self):
        print("Page.fixed is deprecated, please use .parsed!")
        return self.parsed

    @property
    def section_name(self):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(self.text, "lxml")
        spans = soup.find_all("span")

        for span in spans:
            if span.text != "":
                return span.text

            elif not span["id"].startswith("."):
                return span["id"]
