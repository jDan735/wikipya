from typing import TYPE_CHECKING
from ..models import Page, Image
from ..exceptions import NotFound

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def fetch_all(
    self: "MediaWikiAbstract",
    query: str | int,
    to_section: int = 0,
    close_session: bool = True
) -> tuple[Page, Image | None, str | None]:
    self.automatic_session_close = False

    if isinstance(query, int):
        query = await self.get_page_name(query)

    try:
        _, title = await self.check_page(query)
    except NotFound:
        search = await self.search(query)
        title = search[0].title

    opensearch = await self.opensearch(title)
    result = opensearch[0]

    page = await self.page(result.title, to_section=to_section)

    try:
        if self.fetch_image_from_page:
            image = page.fetch_image()
            image.source = self.url.cleaned + image.source
        else:
            image = await self.image(page.title)
    except Exception:
        image = None
 
    if close_session:
        await self.close()

    return page, image, result.link
