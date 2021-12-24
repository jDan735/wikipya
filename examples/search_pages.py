import asyncio
from wikipya import Wikipya


wiki = Wikipya("ru").get_instance()


async def main():
    results = await wiki.search("канобу", limit=5)

    for result in results:
        print(result.title)
        print(result.snippet)
        print(result.page_id)
        print()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
