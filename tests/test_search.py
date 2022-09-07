import pytest
from params import Params
from pytest_lazyfixture import lazy_fixture


@pytest.mark.asyncio
async def test_search(params: Params):
    wiki = params.client

    results = await wiki.search(params.search_query, limit=params.search_limit)
    assert len(results) == params.search_limit


@pytest.mark.parametrize("params", [lazy_fixture("wikipedia")])
@pytest.mark.asyncio
async def test_search_with_description(params: Params):
    wiki = params.client

    results = await wiki.search_with_description("анкап", limit=params.search_limit)

    assert results[0].title == "Анархо-капитализм"
    assert len(results) == params.search_limit


@pytest.mark.asyncio
async def test_opensearch(params: Params):
    wiki = params.client

    results = await wiki.opensearch(params.search_query, params.search_limit)
    assert len(results.results) == params.search_limit
