from ..constants import WGR_FLAG, WRW_FLAG


async def get_all(self, query, lurk=False):
    search = await self.search(query)
    opensearch = await self.opensearch(
        query if lurk else search[0].title
    )

    result = opensearch.results[0]
    page = await self.page(result.title)

    try:
        image = await self.image(page.title)
        image = WRW_FLAG if image.source == WGR_FLAG else image.source

    except Exception:
        image = -1

    return page, image, result.link
