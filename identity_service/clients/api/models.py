import typing as T

from argon2 import PasswordHasher
from pydantic import UUID4, BaseModel


class ClientBase(BaseModel):
    secret: T.Optional[str]
    public_key: T.Optional[bytes]

    @property
    def secret_hash(self) -> T.Optional[bytes]:
        if self.secret is not None:
            password_hasher = PasswordHasher()
            return password_hasher.hash(self.secret).encode()
        return None


class ClientCreateRequest(ClientBase):
    permissions: list = []


class ClientUpdateRequest(ClientBase):
    permissions: T.Optional[list]


class ClientResponse(BaseModel):
    id: UUID4
    public_key: T.Optional[str]
    permissions: list = []
