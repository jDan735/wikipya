from operator import le, lt, eq, gt, ge
from ..exceptions import NotSupported


OPERATORS = {"<=": le, "<": lt, "==": eq, ">": gt, ">=": ge}


class BaseContoller:
    def __init__(self, lang, driver, version, url, host):
        self.lang = lang
        self.driver = driver
        self.version = version
        self.url = url
        self.host = host

        self.thumb = url.replace("api.php", "thumb.php")

        for method in self.METHODS:
            if check_support(version, self.METHODS[method]):
                self.method = getattr(self, method)
                return

        raise NotSupported(f"Not found methods that support MediaWiki v{version}")


def check_support(version, requirement):
    for i in (1, 2):
        try:
            depend = float(requirement[i:])
            operator = requirement[:i]

            break
        except ValueError:
            pass

    return OPERATORS[operator](float(version), depend)
