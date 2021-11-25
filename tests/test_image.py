import pytest
from params import Params


@pytest.mark.asyncio
async def test_image(params: Params):
    page = await params.client.page(params.image_query)
    image = await params.client.image(page.title)

    if params.check_image_res:
        assert image.width > 0
        assert image.height > 0
