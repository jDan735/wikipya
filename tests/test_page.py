import pytest
from pytest_lazyfixture import lazy_fixture

from params import Params


@pytest.mark.parametrize("params", [lazy_fixture("wikipedia")])
@pytest.mark.asyncio
async def test_get_page_name(params: Params):
    wiki = params.client
    name = await wiki.get_page_name(8000432)

    assert name == "Патрик Тёрнер"


@pytest.mark.parametrize("params", [lazy_fixture("wikipedia")])
@pytest.mark.asyncio
async def test_summary(params: Params):
    wiki = params.client
    await wiki.summary("Патрик Тёрнер")
