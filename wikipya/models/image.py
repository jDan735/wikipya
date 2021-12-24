from pydantic import BaseModel
from typing import Optional


class Image(BaseModel):
    source: str
    width: Optional[int]
    height: Optional[int]
