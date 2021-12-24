from ..models import Summary


async def summary(self, title) -> Summary:
    res = await self.driver.get_html(
        f"{self.driver.url.cleaned}api/rest_v1/page/summary/{title}")

    return Summary.parse_raw(res.text)
