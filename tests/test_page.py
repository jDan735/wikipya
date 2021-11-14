import pytest
from pytest_lazyfixture import lazy_fixture

from params import Params


@pytest.mark.parametrize("params", [lazy_fixture("wikipedia")])
@pytest.mark.asyncio
async def test_getPageName(params: Params):
    name = await params.client.getPageName(8000432)

    assert name == "Патрик Тёрнер"
