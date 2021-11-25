import pytest
from params import Params


@pytest.mark.asyncio
async def test_image(params: Params):
    wiki = params.client

    page = await wiki.page(params.image_query)
    image = await wiki.image(page.title)

    if params.check_image_res:
        assert image.width > 0
        assert image.height > 0
