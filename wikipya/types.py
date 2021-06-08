from dataclasses import dataclass


@dataclass
class SearchItem:
    title: str
    pageid: int


@dataclass
class Image:
    source: str
    width: int
    height: int

    def __post_init__(self):
        if self.source.find(".gif") != -1:
            raise TypeError("Gif file")

        if self.source.find("revision/latest/scale-to-width-down") != -1:
            revision = self.source.split("/revision")
            rev = revision[1].split("?")[0]
            size = rev.split("/")[-1]

            new_rev = rev.replace(str(size), "10000")

            self.source = self.source.replace(rev, new_rev)
