from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from identity_service.database import ObjectNotFound, db_session

from ...clients import ClientRepository
from ...configuration import ServiceConfigRepository
from ...enums import IdentityType
from ...models import Identity
from ...token import generate_jwt
from ...users import UserRepository
from .models import (
    AuthenticationResponse,
    ClientAuthenticationRequest,
    UserAuthenticationRequest,
)

router = APIRouter(prefix="/auth")


@router.post(
    "/login",
    response_model=AuthenticationResponse,
    status_code=HTTPStatus.OK,
)
async def login(
    request: UserAuthenticationRequest,
    session: Session = Depends(db_session),
) -> AuthenticationResponse:
    service_config_repository = ServiceConfigRepository(session)
    service_config = service_config_repository.get()
    user_repository = UserRepository(session)
    try:
        user = user_repository.get_by_username(request.username)
        assert request.verify_password(user.password_hash)

    except (AssertionError, ObjectNotFound) as err:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED) from err

    return AuthenticationResponse(
        token=generate_jwt(
            service_config,
            Identity(type=IdentityType.USER, id=user.id, permissions=user.permissions),
            request.audience,
        )
    )


@router.post(
    "/token",
    response_model=AuthenticationResponse,
    status_code=HTTPStatus.OK,
)
async def token(
    request: ClientAuthenticationRequest,
    session: Session = Depends(db_session),
) -> AuthenticationResponse:
    service_config_repository = ServiceConfigRepository(session)
    service_config = service_config_repository.get()
    client_repository = ClientRepository(session)
    try:
        client = client_repository.get_by_id(request.client_id)
        match client.secret_hash, client.public_key:
            case client.secret_hash, None if client.secret_hash is not None:
                assert request.verify_secret(client.secret_hash)

            case None, client.public_key if client.public_key is not None:
                assert request.verify_signature(client.public_key)

            case client.secret_hash, client.public_key if (
                client.secret_hash is not None and client.public_key is not None
            ):
                assert request.verify_secret(
                    client.secret_hash
                ) and request.verify_signature(client.public_key)

            case _:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    except (AssertionError, ObjectNotFound) as err:  # pylint: disable=duplicate-code
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED) from err

    return AuthenticationResponse(
        token=generate_jwt(
            service_config,
            Identity(
                type=IdentityType.CLIENT, id=client.id, permissions=client.permissions
            ),
            request.audience,
        )
    )
