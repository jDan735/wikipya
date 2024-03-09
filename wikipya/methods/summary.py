from ..models import Summary
import json


async def summary(self, title) -> Summary:
    res = await self.driver.get_html(
        f"{self.driver.url.cleaned}api/rest_v1/page/summary/{title}")

    return Summary.model_validate(res.json())
