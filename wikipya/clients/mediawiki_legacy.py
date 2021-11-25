from .mediawiki import MediaWiki
from ..models import Images, Image
from ..exceptions import NotFound

from bs4 import BeautifulSoup


class MediaWiki_Legacy(MediaWiki):
    async def image(self, titles, pithumbsize=1000,
                    piprop="thumbnail", img_blocklist=(),
                    prefix=None, **kwargs):
        r = await self.driver.get(
            action="parse",
            page=titles,
            prop="images",
            redirects="true",
            section=0
        )

        if prefix == "":
            pass
        else:
            prefix = prefix or self.prefix

        _images = Images.parse_obj(r.json["parse"]).images
        images = []

        if len(_images) == 0:
            raise NotFound("Not found images")

        for image in _images:
            if image in img_blocklist:
                continue

            try:
                images.append(await self.get_image(image, prefix=prefix))
                return images[0]
            except Exception as e:
                print(e)

    async def get_image(self, name, prefix="/w"):
        url = self.driver.url.lower() \
                             .replace('/wiki/api.php', self.prefix) \
                             .replace("/w/api.php", self.prefix) \
                             .replace("/api.php", self.prefix)

        status, data, url = await self.driver.get_html(
            f"{url}/File:{name}"
        )

        soup = BeautifulSoup(data, 'lxml')

        file = soup.find("div", id="file")
        thumbnails = soup.find_all("img", {"class": "pi-image-thumbnail"})
        thumbs = soup.find_all("figure", {"class": "thumb"})
        navigation = soup.find_all("nav", {"class": "pi-navigation"})

        if file is not None:
            image = file.a.img
            image["src"] = f"https:{image['src']}"

        elif len(thumbnails) != 0:
            image = thumbnails[0]
            image["src"] = image["srcset"].split()[-2]

        elif len(navigation) != 0:
            image = navigation[0].a.img

        elif len(thumbs) != 0:
            image = thumbs[0].a.img

        else:
            raise NotFound("Not found image")

        return Image(
            source=image["src"],
            width=int(image["width"]), height=int(image["height"])
        )
