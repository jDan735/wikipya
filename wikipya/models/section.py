from pydantic import BaseModel, Field


class Section(BaseModel):
    title: str = Field(alias="line")
    number: str
    index: int
    level: str
    from_title: str = Field(alias="fromtitle")
    bytes_offset: int = Field(alias="byteoffset")
