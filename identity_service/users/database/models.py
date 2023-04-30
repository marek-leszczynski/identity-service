import typing as T

from pydantic import UUID4, BaseModel


class UserCreate(BaseModel):
    id: UUID4
    username: str
    password_hash: str
    is_root: bool
    permissions: list = []


class UserUpdate(BaseModel):
    id: UUID4
    username: T.Optional[str]
    password_hash: T.Optional[str]
    is_root: T.Optional[bool]
    permissions: T.Optional[list]


class UserRead(UserCreate):
    class Config:
        orm_mode = True
