import traceback

try:
    from .aiowiki import Wikipya, NotFound
except ImportError:
    print(traceback.format_exc())


__version__ = "4.0.0b0"
__all__ = ("Wikipya", "NotFound")
