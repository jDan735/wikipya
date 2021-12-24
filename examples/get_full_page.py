import asyncio
from wikipya import Wikipya


wiki = Wikipya("ru").get_instance()


async def main():
    page, image, url = await wiki.get_all("канобу")

    print(page.parsed)
    print(image)
    print(url)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
