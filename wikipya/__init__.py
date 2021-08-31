__version__ = "3.0.0"

try:
    from .aiowiki import Wikipya, NotFound
except Exception as e:
    print(e)
    pass
