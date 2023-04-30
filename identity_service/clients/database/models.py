import typing as T

from pydantic import UUID4, BaseModel


class ClientCreate(BaseModel):
    id: UUID4
    secret_hash: T.Optional[bytes]
    public_key: T.Optional[bytes]
    permissions: list = []


class ClientUpdate(BaseModel):
    id: UUID4
    secret_hash: T.Optional[bytes]
    public_key: T.Optional[bytes]
    permissions: T.Optional[list]


class ClientRead(BaseModel):
    id: UUID4
    secret_hash: T.Optional[str]
    public_key: T.Optional[bytes]
    permissions: list = []

    class Config:
        orm_mode = True
