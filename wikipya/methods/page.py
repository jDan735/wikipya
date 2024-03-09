import contextlib
from ..models import Page
from .lib import query2param


async def page(self, query, section=0, prop="text") -> Page:
    res = await self.driver.get(
        action="parse",
        section=section,
        prop=prop,
        redirects="true",
        **query2param(query),
    )

    with contextlib.suppress(Exception):
        res.json["parse"]["text"] = res.json["parse"]["text"]["*"]

    page = Page.model_validate(res.json["parse"])
    page.tag_blocklist = self.tag_blocklist

    return page
