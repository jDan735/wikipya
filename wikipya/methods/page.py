import contextlib
from ..models import Page
from .lib import query2param


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def page(
    self: "MediaWikiAbstract",
    query: str | int,
    section: int = 0,
    to_section: int = 0,
    prop: str = "text",
) -> Page:
    text = ""
    json = {}

    for i in range(section, to_section + 1):
        _, json = await self.get(
            action="parse",
            section=i,
            prop=prop,
            redirects="true",
            **query2param(query),
        )

        with contextlib.suppress(Exception):
            json["parse"]["text"] = json["parse"]["text"]["*"]

        text += json["parse"]["text"]

    json["parse"]["text"] = text

    page = Page.model_validate(json["parse"])
    page.tag_blocklist = self.tag_blocklist

    return page
