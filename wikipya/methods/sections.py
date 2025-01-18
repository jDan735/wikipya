from .lib import query2param
from ..models import Page


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def sections(self: "MediaWikiAbstract", query: str) -> Page:
    _, json = await self.get(
        action="parse",
        prop="sections",
        redirects="true",
        **query2param(query),
    )

    return Page.model_validate(json["parse"])
