import pytest
from params import Params


@pytest.mark.asyncio
async def test_image(params: Params):
    page = await params.client.page(params.image_query)
    image = await page.image(prefix=params.client.prefix)

    if params.check_image_res:
        assert image.width > 0
        assert image.height > 0
