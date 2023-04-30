import typing as T

from pydantic import BaseModel

from .constants import ERROR_TYPE


class ErrorResponseContent(BaseModel):
    """
    https://tools.ietf.org/html/rfc7807
    """

    type: str = ERROR_TYPE
    title: T.Optional[str]
    status: T.Optional[int]
    detail: T.Optional[str]
    errors: T.Optional[T.List[dict]]
