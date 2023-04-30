import typing as T

from argon2 import PasswordHasher
from pydantic import UUID4, BaseModel


class UserCreateRequest(BaseModel):
    username: str
    password: str
    is_root: bool = False
    permissions: list = []

    @property
    def password_hash(self) -> bytes:
        password_hasher = PasswordHasher()
        return password_hasher.hash(self.password).encode()


class UserUpdateRequest(UserCreateRequest):
    username: T.Optional[str]  # type: ignore[assignment]
    password: T.Optional[str]  # type: ignore[assignment]
    permissions: T.Optional[list]  # type: ignore[assignment]


class UserResponse(BaseModel):
    id: UUID4
    username: str
    is_root: bool
    permissions: list = []
