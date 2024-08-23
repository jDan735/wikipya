import asyncio

import sys

sys.path.insert(0, "..")
from wikipya import Wikipya


wiki = Wikipya(base_url="https://fallout.fandom.com/ru/api.php")


async def main():
    results = await wiki.fandom_search("винт", limit=2)

    from pprint import pprint

    pprint(results)

    for result in results:
        print(result.title)
        print(result.description)
        print(result.page_id)
        print()


if __name__ == "__main__":
    asyncio.run(main())
