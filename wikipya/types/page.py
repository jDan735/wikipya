from tghtml import TgHTML
from ..methods.image import ImageController


class WikipyaPage:
    def __init__(self, parse, params, img_blocklist, lang="en"):
        vars(self).update(parse.__dict__)

        self.blockList = []
        self.lang = lang
        self.params = params      # fastfix for image
        self.img_blocklist = img_blocklist
        self.url = f"https://{lang}.wikipedia.org/w/api.php"
        
        # fix for lurkmore
        if self.text.__class__.__name__ == "JSONObject":
            self.text = self.text.__dict__["*"]

    @property
    def parsed(self):
        return str(TgHTML(self.text, self.blockList, is_wikipedia=False))

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

    async def image(self, pithumbsize=1000, **kwargs):
        return await ImageController(**self.params) \
            .method(self.title, pithumbsize, img_blocklist=self.img_blocklist, **kwargs)
