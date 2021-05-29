class BaseContoller:
    def __init__(self, lang, driver, version, url):
        self.lang = lang
        self.driver = driver
        self.version = version
        self.url = url

        # FIXME: Rewrite this and add version checker
        for method in self.METHODS:
            self.method = getattr(self, method)
