from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from identity_service.database import db_session

from ..database import ClientCreate, ClientRepository, ClientUpdate
from .models import ClientCreateRequest, ClientResponse, ClientUpdateRequest

router = APIRouter(prefix="/clients")


@router.post("", response_model=ClientResponse, status_code=HTTPStatus.CREATED)
async def create_client(
    request: ClientCreateRequest,
    session: Session = Depends(db_session),
) -> ClientResponse:
    client_repository = ClientRepository(session)
    obj = ClientCreate(id=uuid4())
    if request.secret is not None:
        obj.secret_hash = request.secret_hash
    if request.public_key is not None:
        obj.public_key = request.public_key
    if request.permissions:
        obj.permissions = request.permissions

    config = client_repository.create(obj=obj)
    session.commit()
    return ClientResponse(**config.dict())


@router.patch("/{client_id}", response_model=ClientResponse, status_code=HTTPStatus.OK)
async def update_client(
    request: ClientUpdateRequest,
    client_id: UUID4,
    session: Session = Depends(db_session),
) -> ClientResponse:
    client_repository = ClientRepository(session)
    obj = ClientUpdate(id=client_id, **request.dict(exclude_unset=True))
    if request.secret is not None:
        obj.secret_hash = request.secret_hash
    config = client_repository.update(obj=obj)
    session.commit()
    return ClientResponse(**config.dict())


@router.get("/{client_id}", response_model=ClientResponse, status_code=HTTPStatus.OK)
async def get_client(
    client_id: UUID4,
    session: Session = Depends(db_session),
) -> ClientResponse:
    client_repository = ClientRepository(session)
    return ClientResponse(**client_repository.get_by_id(client_id=client_id).dict())
