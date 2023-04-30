import typing as T

from sqlalchemy import types
from sqlalchemy.engine.interfaces import Dialect

from ..encryption import Fernet, decrypt_data_key
from ..settings import settings


class EncryptedField(
    types.TypeDecorator
):  # pylint: disable=abstract-method, too-many-ancestors
    impl = types.LargeBinary

    @staticmethod
    def _encrypt(value: bytes) -> bytes:
        fernet = Fernet(key=settings.data_encryption_key["value"])
        return b":".join(
            [settings.data_encryption_key["cipher_text"], fernet.encrypt(value)]
        )

    @staticmethod
    def _decrypt(value: bytes) -> bytes:
        key, cipher_text = value.split(b":")
        fernet = Fernet(key=decrypt_data_key(settings.encryption_key, key))
        return fernet.decrypt(cipher_text)

    def process_bind_param(
        self, value: T.Optional[str], dialect: Dialect
    ) -> T.Optional[bytes]:
        if value is not None:
            return self._encrypt(value.encode())
        return None

    def process_result_value(
        self, value: T.Optional[bytes], dialect: Dialect
    ) -> T.Optional[bytes]:
        if value is not None:
            return self._decrypt(value)
        return None

    def copy(self, **kw: dict[str, T.Any]) -> "EncryptedField":
        return EncryptedField(self.impl.length)
