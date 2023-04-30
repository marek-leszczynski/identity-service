from pydantic import UUID4, BaseModel

from .enums import IdentityType


class Identity(BaseModel):
    id: UUID4
    type: IdentityType
    permissions: list = []
