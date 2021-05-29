from tghtml import TgHTML
from ..methods.image import Image


class WikipyaPage:
    def __init__(self, parse, params, lang="en"):
        vars(self).update(parse.__dict__)

        self.blockList = []
        self.lang = lang
        self.params = params      # fastfix for image
        self.url = f"https://{lang}.wikipedia.org/w/api.php"

    @property
    def parsed(self):
        return str(TgHTML(self.text, self.blockList))

    @property
    def fixed(self):
        namelist = [
            ["Белоруссия", "Беларусь"],
            ["Белоруссии", "Беларуси"],
            ["Беларуссию", "Беларусь"],
            ["Белоруссией", "Беларусью"],
            ["Белоруссиею", "Беларусью"],

            ["Белору́ссия", "Белару́сь"],
            ["Белору́ссии", "Белару́си"],
            ["Белору́ссию", "Белару́сь"],
            ["Белору́ссией", "Белару́сью"],
            ["Белору́ссиею", "Белару́сью"],


            ["на Украин", "в Украин"],
        ]

        for name in namelist:
            text = self.parsed.replace(*name)

        return text

    async def image(self, pithumbsize=1000):
        return await Image(lang=self.params.lang,
                           driver=self.params.driver,
                           version=self.params.version,
                           url=self.params.url) \
            .method(self.title, pithumbsize)
