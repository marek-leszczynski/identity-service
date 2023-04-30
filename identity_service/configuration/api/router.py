import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends
from jwcrypto import jwk
from sqlalchemy.orm import Session

from identity_service.configuration.database.models import ServiceConfigUpdate

from ...database import db_session
from ..database import ServiceConfigCreate, ServiceConfigRepository
from .models import (
    ServiceConfigCreateRequest,
    ServiceConfigResponse,
    ServiceConfigUpdateRequest,
)

router = APIRouter(prefix="/configuration")


@router.post("", response_model=ServiceConfigResponse, status_code=HTTPStatus.CREATED)
async def create_configuration(
    request: ServiceConfigCreateRequest,
    session: Session = Depends(db_session),
) -> ServiceConfigResponse:
    service_config_repository = ServiceConfigRepository(session)
    config = service_config_repository.create(
        obj=ServiceConfigCreate(id=uuid.uuid4(), **request.dict())
    )
    session.commit()
    return ServiceConfigResponse(**config.dict())


@router.patch("", response_model=ServiceConfigResponse, status_code=HTTPStatus.CREATED)
async def update_configuration(
    request: ServiceConfigUpdateRequest,
    session: Session = Depends(db_session),
) -> ServiceConfigResponse:
    service_config_repository = ServiceConfigRepository(session)
    config = service_config_repository.update(
        obj=ServiceConfigUpdate(**request.dict(exclude_unset=True))
    )
    session.commit()
    return ServiceConfigResponse(**config.dict())


@router.get("", response_model=ServiceConfigResponse, status_code=HTTPStatus.CREATED)
async def get_configuration(
    session: Session = Depends(db_session),
) -> ServiceConfigResponse:
    service_config_repository = ServiceConfigRepository(session)
    return ServiceConfigResponse(**service_config_repository.get().dict())


@router.get("/jwks", status_code=HTTPStatus.CREATED)
async def get_jwks(
    session: Session = Depends(db_session),
) -> dict:
    service_config_repository = ServiceConfigRepository(session)
    config = service_config_repository.get()
    jwk_instance = jwk.JWK.from_pem(config.public_key)
    jwk_instance.update(use="sig", alg="RS256")
    return jwk_instance.export_public(as_dict=True)
