from ..exceptions import NotFound
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def get_page_name(self: "MediaWikiAbstract", id: int) -> str:
    _, json = await self.get(pageids=id)

    try:
        return json["query"]["pages"][-1]["title"]
    except AttributeError:
        raise NotFound(f"Not found page with this id: {id}")
