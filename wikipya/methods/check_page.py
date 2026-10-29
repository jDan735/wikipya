from ..exceptions import NotFound

from msgspec import defstruct, Struct, field

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


class PageQuery(Struct, frozen=True):
    class Page(Struct, frozen=True):
        title: str
        id: int = field(name="pageid", default=0)
        missing: bool = False

    query: defstruct("PagesList", [("pages", list[Page])], frozen=True)


async def check_page(self: "MediaWikiAbstract", query: str) -> tuple[int, str]:
    _, res = await self.get(
        titles=query,
        type=PageQuery,
    )

    for page in res.query.pages:
        if page.missing:
            continue
        return page.id, page.title

    raise NotFound("Couldn't find page by title")
