from ..drivers import HttpxDriver


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