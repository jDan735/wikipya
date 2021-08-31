from .drivers import HttpxDriver
from .types import SearchItem, WikipyaPage, Image, OpenSearchResult

from .exceptions import NotFound

from bs4 import BeautifulSoup


class BaseClient:
    def __init__(self, driver=HttpxDriver, url=None, lang="ru"):
        self.driver = driver(
            (url or self.BASE_URL).format(lang=lang),
            params=self.DEFAULT_PARAMS
        )

    async def search(self, *args, **kwargs):
        raise NotImplementedError

    async def opensearch(self, *args, **kwargs):
        raise NotImplementedError

    async def page(self, *args, **kwargs):
        raise NotImplementedError

    async def _page(self, *args, **kwargs):
        raise NotImplementedError

    async def image(self, *args, **kwargs):
        raise NotImplementedError

    async def get_all(self, *args, **kwargs):
        raise NotImplementedError

    async def getPageName(self, *args, **kwargs):
        raise NotImplementedError


class MediaWiki(BaseClient):
    DEFAULT_PARAMS = {
        "format": "json",
        "action": "query",
        "formatversion": 2
    }

    BASE_URL = "https://{lang}.wikipedia.org/w/api.php"
    LANG = None

    WGR_FLAG = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb" +
        "/8/85/Flag_of_Belarus.svg/1000px-Flag_of_Belarus.svg.png"
    )

    WRW_FLAG = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb" +
        "/5/50/Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg" +
        "/1000px-Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg.png"
    )

    async def search(self, query, limit=1, prop="size"):
        res = await self.driver.get(
            list="search",
            srsearch=query,
            srlimit=limit,
            srprop=prop
        )

        if len(res.query.search) == 0:
            raise NotFound("Search can't find anything on your request")

        return [SearchItem(
            title=item.__dict__.get("title"),
            pageid=item.__dict__.get("pageid")
        ) for item in res.query.search]

    async def opensearch(self, query, limit=1):
        res = OpenSearchResult(*await self.driver.get(
            action="opensearch",
            search=query,
            limit=limit,
        ))

        if len(res.variants) == 0:
            raise NotFound("OpenSearch can't find anything on your request")

        return res

    async def page(self, query, section=0, prop="text", blocklist=()):
        if query.__class__ == str:
            params = {"page": query}

        elif query.__class__ == int:
            params = {"pageid": query}

        elif query.pageid is not None:
            params = {"pageid": query.pageid}

        else:
            params = {"page": query.title}

        res = await self.driver.get(
            action="parse",
            section=section,
            prop=prop,
            redirects="true",
            **params,
        )

        return WikipyaPage(res.parse, lang=self.LANG, _image=self.image,
                           tag_blocklist=blocklist)

    async def image(self, titles, pithumbsize=1000,
                    piprop="thumbnail", img_blocklist=(), prefix=None):
        res = await self.driver.get(
            titles=titles,
            prop="pageimages",
            pilicense="any",
            pithumbsize=pithumbsize,
            piprop=piprop,
        )

        try:
            image = res.query.pages[-1]
            thumb = image.thumbnail

            return Image(**thumb.__dict__)

        except AttributeError:
            raise NotFound("Not found image")

    async def getPageName(self, id_):
        res = await self.driver.get(
            pageids=id_
        )

        try:
            return res.query.pages[-1].title
        except AttributeError:
            raise NotFound(f"Not found page with this id: {id_}")

    async def get_all(self, query, lurk=False,
                      blocklist=(), prefix="w", img_blocklist=(), **kwargs):
        search = await self.search(query)
        opensearch = await self.opensearch(
            query if lurk else search[0].title
        )

        variant = opensearch.variants[0]
        page = await self.page(variant.title, blocklist=blocklist)

        try:
            image = await page.image(prefix=prefix,
                                     img_blocklist=img_blocklist)
            image = image.source

        except Exception as e:
            image = -1

        if image == self.WGR_FLAG:
            image = self.WRW_FLAG

        return page, image, variant.link


class MediaWiki_Legacy(MediaWiki):
    DEFAULT_PARAMS = {
        "format": "json",
        "action": "query",
        "formatversion": 2
    }

    LANG = None

    async def image(self, titles, pithumbsize=1000,
                    piprop="thumbnail", img_blocklist=(),
                    prefix="/w", **kwargs):
        data = await self.driver.get(
            action="parse",
            page=titles,
            prop="images",
            redirects="true",
            section=0
        )

        all_images = data.parse.images

        if len(all_images) == 0:
            raise NotFound("Not found images")
        
        images = []

        for image in all_images:
            if image in img_blocklist:
                continue

            try:
                images.append(await self.get_image(image, prefix=prefix))
                return images[0]
            except Exception as e:
                print(e)

    async def get_image(self, name, prefix="/w"):
        url = self.driver.url.lower() \
                             .replace('/wiki/api.php', prefix) \
                             .replace("/w/api.php", prefix) \
                             .replace("/api.php", prefix)

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


class MediaWiki_Lurk(MediaWiki_Legacy):
    DEFAULT_PARAMS = {
        "format": "json",
        "action": "query",
        "formatversion": 2
    }

    LANG = None
