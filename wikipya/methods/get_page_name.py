from ..exceptions import NotFound


async def get_page_name(self, id) -> str:
    res = await self.driver.get(pageids=id)

    try:
        return res.json["query"]["pages"][-1]["title"]
    except AttributeError:
        raise NotFound(f"Not found page with this id: {id}")
