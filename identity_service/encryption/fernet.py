import base64
import binascii
import os
import typing as T

from cryptography.fernet import Fernet as BaseFernet


class Fernet(BaseFernet):
    def __init__(  # pylint: disable=super-init-not-called
        self, key: T.Union[bytes, str]
    ):
        try:
            key = base64.urlsafe_b64decode(key)
        except binascii.Error as exc:
            raise ValueError(
                "Fernet key must be 64 url-safe base64-encoded bytes."
            ) from exc
        if len(key) != 64:
            raise ValueError("Fernet key must be 64 url-safe base64-encoded bytes.")

        self._signing_key = key[:32]
        self._encryption_key = key[32:]

    @classmethod
    def generate_key(cls) -> bytes:
        return base64.urlsafe_b64encode(os.urandom(64))
