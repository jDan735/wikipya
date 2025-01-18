from typing import Any, Union
from ..models import SearchResult


def query2param(query: Union[str, int, SearchResult]) -> Any:
    if query.__class__ is str:
        return {"page": query}
    elif query.__class__ is int:
        return {"pageid": query}
    elif query.pageid is not None:  # type: ignore
        return {"pageid": query.pageid}  # type: ignore
    else:
        return {"page": query.title}  # type: ignore
