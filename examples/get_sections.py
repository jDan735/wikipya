import asyncio
from wikipya import Wikipya


wiki = Wikipya("ru").get_instance()


async def main():
    sections = await wiki.sections("канобу")

    for section in sections.sections:
        print(section.number, section.title)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
