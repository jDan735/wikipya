from ..models import Image
from ..exceptions import NotFound


async def image(self, titles, pithumbsize=1000) -> Image:
    res = await self.driver.get(
        titles=titles,
        prop="pageimages",
        pilicense="any",
        pithumbsize=pithumbsize,
        piprop="thumbnail",
    )

    try:
        image = res.json["query"]["pages"][-1]
        thumb = image["thumbnail"]

        return Image(**thumb)
    except AttributeError:
        raise NotFound("Not found image")
