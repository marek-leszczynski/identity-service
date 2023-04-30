import typing as T

from pydantic import BaseModel, PositiveInt


class ServiceConfigCreateRequest(BaseModel):
    public_key: str
    private_key: str
    jwt_expiration: PositiveInt
    jwt_max_refreshes: PositiveInt
    jwt_issuer: str


class ServiceConfigUpdateRequest(BaseModel):
    public_key: T.Optional[str]
    private_key: T.Optional[str]
    jwt_expiration: T.Optional[PositiveInt]
    jwt_max_refreshes: T.Optional[PositiveInt]
    jwt_issuer: T.Optional[str]


class ServiceConfigResponse(ServiceConfigCreateRequest):
    ...
