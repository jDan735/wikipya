import pytest


class CommonTestsWikipya:
    ALLOW_HTTP = False
    SEARCH_QUERY = "cmake"
    SEARCH_LIMIT = 4
    IMAGE_QUERY = "Украина"
    CHECK_IMAGE_RES = True

    def test_https(self):
        # Use HTTPS instead of HTTP, please. Ignore with ALLOW_HTTP

        is_https_used = self.wikipya.url.startswith("https://")
        assert self.ALLOW_HTTP or is_https_used

    @pytest.mark.asyncio
    async def test_search(self):
        results = await self.wikipya.search(self.SEARCH_QUERY, limit=self.SEARCH_LIMIT)

        assert len(results) == self.SEARCH_LIMIT

    @pytest.mark.asyncio
    async def test_opensearch(self):
        results = await self.wikipya.opensearch(self.SEARCH_QUERY, limit=self.SEARCH_LIMIT)

        assert len(results) == self.SEARCH_LIMIT

    @pytest.mark.asyncio
    async def test_image(self):
        page = await self.wikipya.page(self.IMAGE_QUERY)
        image = await page.image()

        if self.CHECK_IMAGE_RES:
            assert image.width > 0
            assert image.height > 0


    @pytest.mark.asyncio
    async def test_getPageName(self):
        name = await self.wikipya.getPageName(8000432)

        assert name == "Патрик Тёрнер"

    @pytest.mark.asyncio
    async def test_page(self):
        page = await self.wikipya.page(self.SEARCH_QUERY)

        for _ in page.text, page.fixed, page.parsed:
            assert _ != ""