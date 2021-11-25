from pydantic import BaseModel


class Images(BaseModel):
    title: str
    images: list[str]
