__version__ = "3.0.0b3"

try:
    from .aiowiki import Wikipya, NotFound
except Exception as e:
    print(e)
    pass
