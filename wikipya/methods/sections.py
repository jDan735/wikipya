from .lib import query2param
from ..models import Page


async def sections(self, query) -> Page:
    res = await self.driver.get(
        action="parse",
        prop="sections",
        redirects="true",
        **query2param(query),
    )

    page = Page.parse_obj(res.json["parse"])
    return page
