import functools

from .fernet import Fernet


@functools.cache
def decrypt_data_key(master_key: bytes, value: bytes) -> bytes:
    fernet = Fernet(key=master_key)
    return fernet.decrypt(value)


def encrypt_data_key(master_key: bytes, value: bytes) -> bytes:
    fernet = Fernet(key=master_key)
    return fernet.encrypt(value)


# def encrypt(value: bytes, key: bytes) -> bytes:
#     fernet = Fernet(key=decrypt_data_key(key))
#     return fernet.encrypt(value)


# def decrypt(value: bytes, key: bytes) -> bytes:
#     fernet = Fernet(key=decrypt_data_key(key))
#     return fernet.decrypt(value)
