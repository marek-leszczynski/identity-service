from enum import Enum


class AuthenticationType(str, Enum):
    RSA = "rsa"
    SECRET = "secret"
    RSA_SECRET = "rsa_secret"
