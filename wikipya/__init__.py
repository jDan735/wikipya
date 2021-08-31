__version__ = "3.0.1"

try:
    from .aiowiki import Wikipya, NotFound
    from . import clients
except Exception as e:
    print(e)
    pass
