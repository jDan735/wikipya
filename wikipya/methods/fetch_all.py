from typing import TYPE_CHECKING
from ..models import Page, Image
from ..exceptions import NotFound

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def fetch_all(
    self: "MediaWikiAbstract", query: str | int, to_section: int = 0
) -> tuple[Page, Image | None, str | None]:
    if isinstance(query, int):
        query = await self.get_page_name(query)

    search = await self.search(query)
    opensearch = await self.opensearch(search[0].title)

    result = opensearch.results[0]
    page = await self.page(result.title, to_section=to_section)

    try:
        image = await self.image(page.title)
    except (NotFound, KeyError):
        image = None

    return page, image, result.link
