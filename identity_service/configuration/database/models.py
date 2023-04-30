import typing as T

from pydantic import UUID4, BaseModel, PositiveInt


class ServiceConfigCreate(BaseModel):
    id: UUID4
    public_key: bytes
    private_key: bytes
    jwt_expiration: PositiveInt
    jwt_issuer: str
    jwt_max_refreshes: PositiveInt


class ServiceConfigUpdate(BaseModel):
    public_key: T.Optional[bytes]
    private_key: T.Optional[bytes]
    jwt_expiration: T.Optional[PositiveInt]
    jwt_issuer: T.Optional[str]
    jwt_max_refreshes: T.Optional[PositiveInt]


class ServiceConfigRead(ServiceConfigCreate):
    class Config:
        orm_mode = True
