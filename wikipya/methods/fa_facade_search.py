from typing import TYPE_CHECKING

from ..exceptions import NotFound
from ..models import Suggestion


if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def fandom_facade_search(
    self: "MediaWikiAbstract", query: str, limit: int = 1, prop: str = "snippet"
) -> list[Suggestion]:
    try:
        return await self.fandom_search(query, limit)
    except NotFound:
        return await self.legacy_search(query, limit, prop)


__all__ = ("fandom_facade_search",)
