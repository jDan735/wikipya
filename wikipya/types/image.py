from dataclasses import dataclass


@dataclass
class Image:
    source: str
    width: int
    height: int
