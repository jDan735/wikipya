from .base import BaseContoller
from ..exceptions import NotFound
from ..types.image import ImageItem


class Image(BaseContoller):
    METHODS = {
        "image": ">=1.0"
    }

    async def image(self, titles, pithumbsize=1000, **kwargs):
        status, data = await self.driver.get(
            titles=titles,
            prop="pageimages",
            pilicense="any",
            pithumbsize=pithumbsize,
            **kwargs
        )

        try:
            image = data.query.pages[-1]
            thumb = image.thumbnail

            return ImageItem(**thumb.__dict__)

        except AttributeError:
            raise NotFound("Not found image")
