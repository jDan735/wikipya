from bs4 import BeautifulSoup

from ..models import Image, Images
from ..exceptions import NotFound


__all__ = ("legacy_image", "get_images_list", "get_image")


async def legacy_image(self, titles, pithumbsize=1000) -> Image:
    _images = await self.get_images_list(titles)
    images = []

    if len(_images) == 0:
        raise NotFound("Not found images")

    for image in _images:
        if image in self.img_blocklist:
            continue

        try:
            images.append(await self.get_image(image))
            return images[0]
        except Exception as e:
            print(e)


async def get_images_list(self, titles) -> list[str]:
    r = await self.driver.get(
        action="parse",
        page=titles,
        prop="images",
        redirects="true",
        section=0
    )

    return Images.parse_obj(r.json["parse"]).images


async def get_image(self, name) -> Image:
    r = await self.driver.get_html(f"{self.url.image_url}/File:{name}")
    soup = BeautifulSoup(r.text, 'lxml')

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
