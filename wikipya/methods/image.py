from .base import BaseContoller
from ..exceptions import NotFound
from ..types.image import Image

from bs4 import BeautifulSoup


class ImageController(BaseContoller):
    METHODS = {
        "image": ">=1.25",
        "parse_images": ">=1.0"
    }

    async def image(self, titles, pithumbsize=1000,
                    piprop="thumbnail", img_blocklist=(), **kwargs):
        status, data = await self.driver.get(
            titles=titles,
            prop="pageimages",
            pilicense="any",
            pithumbsize=pithumbsize,
            piprop=piprop,
            **kwargs
        )

        try:
            image = data.query.pages[-1]
            thumb = image.thumbnail

            return Image(**thumb.__dict__)

        except AttributeError:
            raise NotFound("Not found image")

    async def parse_images(self, titles, pithumbsize=1000,
                           piprop="thumbnail", img_blocklist=(), **kwargs):
        status, data = await self.driver.get(
            action="parse",
            page=titles,
            prop="images",
            redirects="true",
            section=0
        )

        all_images = data.parse.images

        if len(all_images) == 0:
            raise NotFound("Not found image")
        else:
            images = []

            for image in all_images:
                if not image in img_blocklist:
                    try:
                        images.append(await self.get_image(image))
                    except Exception as e:
                        print(e)

            return images[0]

    async def get_image(self, name):
        status, data, url = await self.driver.get_html(
            f"{self.url.replace('/api.php', '')}/File:{name}"
        )

        if str(url).endswith("/404.html"):
            status, data, url = await self.driver.get_html(
                f"{self.url.replace('w/api.php', '')}wiki/File:{name}"
            )

        if status != 200:
            return 404

        soup = BeautifulSoup(data, 'lxml')

        file = soup.find("div", id="file")
        thumbnails = soup.find_all("img", {"class": "pi-image-thumbnail"})
        
        if file is not None:
            return Image(
                source="https:" + self.host + soup.find("div", id="file").a.img["src"],
                width=0, height=0
            )
        elif len(thumbnails) != 0:
            image = thumbnails[0]

            return Image(
                source=image["srcset"].split()[-2],
                width=image["width"], height=image["height"]
            )
