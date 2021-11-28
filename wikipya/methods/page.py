from ..models import Page


async def page(self, query, section=0, prop="text") -> Page:
    if query.__class__ == str:
        params = {"page": query}
    elif query.__class__ == int:
        params = {"pageid": query}
    elif query.pageid is not None:
        params = {"pageid": query.pageid}
    else:
        params = {"page": query.title}

    res = await self.driver.get(
        action="parse",
        section=section,
        prop=prop,
        redirects="true",
        **params,
    )

    try:
        res.json["parse"]["text"] = res.json["parse"]["text"]["*"]
    except Exception:
        pass

    page = Page.parse_obj(res.json["parse"])
    page.tag_blocklist = self.tag_blocklist

    return page
