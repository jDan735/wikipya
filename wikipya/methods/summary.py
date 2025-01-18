from ..models import Summary

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def summary(self: "MediaWikiAbstract", title: str) -> Summary:
    res = await self.get_html(f"{self.url.cleaned}api/rest_v1/page/summary/{title}")

    return Summary.model_validate(res.json())
