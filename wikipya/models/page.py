from pydantic import BaseModel, Field
from tghtml import TgHTML

from bs4 import BeautifulSoup

from typing import Optional

from .section import Section


class Page(BaseModel):
    title: str
    pageid: Optional[int]

    text: Optional[str]
    sections: Optional[list[Section]]

    tag_blocklist: Optional[list] = Field(repr=False)

    @property
    def parsed(self):
        return TgHTML(self.text, self.tag_blocklist).parsed.strip()

    @property
    def fixed(self):
        print("Page.fixed is deprecated, please use .parsed!")
        return self.parsed

    @property
    def section_name(self):
        soup = BeautifulSoup(self.text, "lxml")
        spans = soup.find_all("span")

        for span in spans:
            if span.text != "":
                return span.text

            elif not span["id"].startswith("."):
                return span["id"]
