import datetime
import typing as T

from jwcrypto import jwt

from .configuration import ServiceConfigRead
from .models import Identity


def generate_jwt(
    service_config: ServiceConfigRead, identity: Identity, audience: T.Optional[str]
) -> str:
    iat = datetime.datetime.now(tz=datetime.timezone.utc)
    payload = {
        "iss": service_config.jwt_issuer,
        "iat": int(iat.timestamp()),
        "exp": int(
            (
                iat + datetime.timedelta(seconds=service_config.jwt_expiration)
            ).timestamp()
        ),
        "sub": str(identity.id),
        "aud": audience,
        "gty": f"{identity.type.value}-credentials",
        "permissions": identity.permissions,
    }
    key = jwt.JWK.from_pem(service_config.private_key)
    token = jwt.JWT(
        header={"alg": "RS256", "typ": "JWT", "kid": key.key_id}, claims=payload
    )
    token.make_signed_token(key)

    return token.serialize()
