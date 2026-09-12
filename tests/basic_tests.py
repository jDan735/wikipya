from unittest import IsolatedAsyncioTestCase
from wikipya import Wikipya
from parameterized import parameterized
from .clients import clients, Params


class Test(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        for client in clients:
            client[0].open()

    async def asyncTearDown(self):
        for client in clients:
            await client[0].close()

    @parameterized.expand(clients)
    def test_https(self, client: Wikipya, params: Params):
        """Check HTTPS usage instead of HTTP. Ignore with ALLOW_HTTP"""
        is_https_used = client.url.base_url.startswith("https://")
        assert params.allow_http or is_https_used

    @parameterized.expand(clients)
    async def test_search(self, client: Wikipya, params: Params):
        results = await client.search(
            params.search_query,
            limit=params.search_limit,
        )
        assert len(results) == params.search_limit

    @parameterized.expand([clients[0]])
    async def test_search_with_description(self, client: Wikipya, params: Params):
        results = await client.search_with_description(
            "анкап", limit=params.search_limit
        )

        assert results[0].title == "Анархо-капитализм"
        assert len(results) == params.search_limit

    @parameterized.expand(clients)
    async def test_opensearch(self, client: Wikipya, params: Params):
        results = await client.opensearch(params.search_query, params.search_limit)
        assert len(results.results) == params.search_limit

    @parameterized.expand([clients[0]])
    async def test_get_page_name(self, client: Wikipya, params: Params):
        name = await client.get_page_name(8000432)
        assert name == "Патрик Тёрнер"

    @parameterized.expand([clients[0]])
    async def test_summary(self, client: Wikipya, params: Params):
        await client.summary("Патрик Тёрнер")

    @parameterized.expand(clients)
    async def test_image(self, client: Wikipya, params: Params):
        image = await client.image(params.image_query)

        if params.check_image_res:
            assert image.width > 0
            assert image.height > 0
