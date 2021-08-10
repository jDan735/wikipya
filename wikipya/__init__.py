__version__ = "3.0.0b6"

try:
    from .aiowiki import Wikipya, NotFound
except Exception as e:
    print(e)
    pass
