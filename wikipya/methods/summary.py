from ..models import Summary

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def summary(self: "MediaWikiAbstract", title: str) -> Summary:
    _, res = await self.get(
        f"/api/rest_v1/page/summary/{title}",
        type=Summary,
    )

    return res
