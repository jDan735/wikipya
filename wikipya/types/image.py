from dataclasses import dataclass


@dataclass
class ImageItem:
    source: str
    width: int
    height: int
