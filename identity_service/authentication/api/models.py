import base64
import typing as T

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from pydantic import UUID4, BaseModel


class UserAuthenticationRequest(BaseModel):
    username: str
    password: str
    audience: T.Optional[str]

    def verify_password(self, password_hash: str) -> bool:
        password_hasher = PasswordHasher()
        try:
            return password_hasher.verify(password_hash, self.password)
        except VerifyMismatchError:
            return False


class ClientAuthenticationRequest(BaseModel):
    client_id: UUID4
    client_secret: T.Optional[str]
    signature: T.Optional[str]
    audience: str

    def verify_secret(self, client_secret_hash: str) -> bool:
        if self.client_secret is None:
            return False

        password_hasher = PasswordHasher()
        try:
            return password_hasher.verify(client_secret_hash, self.client_secret)
        except VerifyMismatchError:
            return False

    def verify_signature(self, public_key: bytes) -> bool:
        if self.signature is None:
            return False

        try:
            key = serialization.load_pem_public_key(
                public_key, backend=default_backend()
            )
            T.cast(rsa.RSAPublicKey, key).verify(
                base64.b64decode(self.signature),
                str(self.client_id).encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
        except InvalidSignature:
            return False
        return True


class AuthenticationResponse(BaseModel):
    token: str
    audience: T.Optional[str]
