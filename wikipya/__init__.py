try:
    from .aiowiki import Wikipya, NotFound
except ImportError:
    pass


__version__ = "4.0.0b0"
__all__ = ("Wikipya", "NotFound")
