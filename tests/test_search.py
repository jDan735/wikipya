import pytest
from params import Params


@pytest.mark.asyncio
async def test_search(params: Params):
    results = await params.client.search(
        params.search_query, limit=params.search_limit)

    assert len(results) == params.search_limit


@pytest.mark.asyncio
async def test_opensearch(params: Params):
    results = await params.client.opensearch(
        params.search_query, params.search_limit)

    assert len(results.variants) == params.search_limit
