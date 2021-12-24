import pytest
from params import Params


@pytest.mark.asyncio
async def test_search(params: Params):
    wiki = params.client

    results = await wiki.search(params.search_query, limit=params.search_limit)
    assert len(results) == params.search_limit


@pytest.mark.asyncio
async def test_opensearch(params: Params):
    wiki = params.client

    results = await wiki.opensearch(params.search_query, params.search_limit)
    assert len(results.results) == params.search_limit
