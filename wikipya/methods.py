from operator import le, lt, eq, gt, ge

from .exceptions import NotFound, NotSupported
from .types import Image

from bs4 import BeautifulSoup


OPERATORS = {"<=": le, "<": lt, "==": eq, ">": gt, ">=": ge}


class BaseContoller:
    def __init__(self, lang, driver, version, url, host):
        self.lang = lang
        self.driver = driver
        self.version = version
        self.url = url
        self.host = host

        self.thumb = url.replace("api.php", "thumb.php")

        for method in self.METHODS:
            if check_support(version, self.METHODS[method]):
                self.method = getattr(self, method)
                return

        raise NotSupported(f"Not found methods that support MediaWiki v{version}")


def check_support(version, requirement):
    for i in (1, 2):
        try:
            depend = float(requirement[i:])
            operator = requirement[:i]

            break
        except ValueError:
            pass

    return OPERATORS[operator](float(version), depend)


class ImageController(BaseContoller):
    METHODS = {
        "image": ">=1.25",
        "parse_images": ">=1.0"
    }

    async def image(self, titles, pithumbsize=1000,
                    piprop="thumbnail", img_blocklist=(), prefix="w",
                    **kwargs):
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
                           piprop="thumbnail", img_blocklist=(),
                           prefix="w", **kwargs):
        status, data = await self.driver.get(
            action="parse",
            page=titles,
            prop="images",
            redirects="true",
            section=0
        )

        all_images = data.parse.images

        if len(all_images) == 0:
            raise NotFound("Not found images")
        else:
            images = []

            for image in all_images:
                if image not in img_blocklist:
                    try:
                        images.append(await self.get_image(
                                          image,
                                          prefix=prefix))
                        return images[0]
                    except Exception as e:
                        print(e)

    async def get_image(self, name, prefix="w"):
        url = self.url.lower() \
                      .replace('/wiki/api.php', prefix) \
                      .replace("/w/api.php", prefix) \
                      .replace("/api.php", prefix) \

        status, data, url = await self.driver.get_html(
            f"{url}/File:{name}"
        )

        if status != 200:
            return 404

        soup = BeautifulSoup(data, 'lxml')

        file = soup.find("div", id="file")
        thumbnails = soup.find_all("img", {"class": "pi-image-thumbnail"})
        thumbs = soup.find_all("figure", {"class": "thumb"})
        navigation = soup.find_all("nav", {"class": "pi-navigation"})

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

        elif len(navigation) != 0:
            image = navigation[0].a.img

        elif len(thumbs) != 0:
            image = thumbs[0].a.img

        else:
            raise NotFound("Not found image")

        return Image(
            source=image["src"],
            width=image["width"], height=image["height"]
        )
