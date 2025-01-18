from ..models import Image
from ..exceptions import NotFound


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clients import MediaWikiAbstract


async def image(
    self: "MediaWikiAbstract", titles: str, pithumbsize: int = 1000
) -> Image:
    _, json = await self.get(
        titles=titles,
        prop="pageimages",
        pilicense="any",
        pithumbsize=pithumbsize,
        piprop="thumbnail",
    )

    try:
        image = json["query"]["pages"][-1]
        thumb = image["thumbnail"]

        return Image(**thumb)
    except AttributeError as e:
        raise NotFound("Not found image") from e
