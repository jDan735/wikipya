import unittest
import asyncio

from wikipya.aiowiki import Wikipya

wiki = Wikipya("ru")


def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        except RuntimeError:
            pass
    return wrapper


class TestWikipya(unittest.TestCase):
    @async_test
    async def test_search(self):
        search = await wiki.search("cmake", limit=4)
        self.assertEqual(len(search), 4)

    @async_test
    async def test_opensearch(self):
        opensearch = await wiki.opensearch("test", limit=4)
        self.assertEqual(len(opensearch[0]), 4)

    @async_test
    async def test_image(self):
        page = await wiki.page("канобу")
        image = await page.image()

        self.assertTrue(image.width > 0)
        self.assertTrue(image.height > 0)

    @async_test
    async def test_getPageName(self):
        name = await wiki.getPageName(8000432)
        self.assertEqual(name, "Патрик Тёрнер")

    @async_test
    async def test__page(self):
        search = await wiki.search("cmake")
        page = await wiki._page(search[0])

        for item in page.text, page.fixed, page.parsed:
            self.assertTrue(item != "")

    @async_test
    async def test_page(self):
        page = await wiki.page("cmake")

        for item in page.text, page.fixed, page.parsed:
            self.assertTrue(item != "")
