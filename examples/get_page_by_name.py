import asyncio
from wikipya import Wikipya


wiki = Wikipya("ru").get_instance()


async def main():
    page = await wiki.page("путин")

    print(page.title)
    print(page.parsed[:200])


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
