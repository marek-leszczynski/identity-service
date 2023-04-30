import functools
import typing as T

from pydantic import BaseSettings
from sqlalchemy.engine import URL

from .encryption import Fernet, encrypt_data_key


class Settings(BaseSettings):
    allowed_origins: T.List[str]

    database_host: str
    database_username: str
    database_password: str
    database_schema_name: str
    database_port: int = 5432
    database_driver: str = "postgresql+psycopg2"
    database_connection_pool_size: int = 5
    database_connection_max_overflow: int = 10
    database_ssl_mode: str = "require"
    database_ssl_root_cert: T.Optional[str]
    database_ssl_cert: T.Optional[str]
    database_ssl_key: T.Optional[str]
    encryption_key: bytes

    class Config:
        keep_untouched = (functools.cached_property,)

    @functools.cached_property
    def data_encryption_key(self) -> dict:
        key = Fernet.generate_key()
        return {"value": key, "cipher_text": encrypt_data_key(self.encryption_key, key)}

    @property
    def url(self) -> URL:
        string_params = {
            "sslmode": self.database_ssl_mode,
            "sslrootcert": self.database_ssl_root_cert,
            "sslcert": self.database_ssl_cert,
            "sslkey": self.database_ssl_key,
        }

        return URL.create(
            drivername=self.database_driver,
            username=self.database_username,
            password=self.database_password,
            database=self.database_schema_name,
            host=self.database_host,
            port=self.database_port,
            query={
                key: value for key, value in string_params.items() if value is not None
            },
        )


settings = Settings()
