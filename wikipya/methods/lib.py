from typing import Union
from ..models import SearchResult


def query2param(query: Union[str, int, SearchResult]) -> dict:
    if query.__class__ is str:
        return {"page": query}
    elif query.__class__ is int:
        return {"pageid": query}
    elif query.pageid is not None:
        return {"pageid": query.pageid}
    else:
        return {"page": query.title}
