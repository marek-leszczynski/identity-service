from enum import Enum


class IdentityType(str, Enum):
    CLIENT = "client"
    USER = "user"
