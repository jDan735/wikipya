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

    try:
        res.json["parse"]["text"] = res.json["parse"]["text"]["*"]
    except Exception:
        pass

    page = Page.parse_obj(res.json["parse"])
    page.tag_blocklist = self.tag_blocklist

    return page
