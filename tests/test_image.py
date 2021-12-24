import pytest
from params import Params


@pytest.mark.asyncio
async def test_image(params: Params):
    wiki = params.client
    image = await wiki.image(params.image_query)

    if params.check_image_res:
        assert image.width > 0
        assert image.height > 0
