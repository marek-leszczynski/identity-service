from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from ...database import db_session
from ..database import UserCreate, UserRepository, UserUpdate
from .models import UserCreateRequest, UserResponse, UserUpdateRequest

router = APIRouter(prefix="/users")


@router.post("", response_model=UserResponse, status_code=HTTPStatus.CREATED)
async def create_user(
    request: UserCreateRequest,
    session: Session = Depends(db_session),
) -> UserResponse:
    client_repository = UserRepository(session)
    config = client_repository.create(
        obj=UserCreate(
            id=uuid4(), password_hash=request.password_hash, **request.dict()
        )
    )
    session.commit()
    return UserResponse(**config.dict())


@router.patch("/{user_id}", response_model=UserResponse, status_code=HTTPStatus.OK)
async def update_user(
    request: UserUpdateRequest,
    user_id: UUID4,
    session: Session = Depends(db_session),
) -> UserResponse:
    user_repository = UserRepository(session)
    user = user_repository.update(
        obj=UserUpdate(id=user_id, **request.dict(exclude_unset=True))
    )
    session.commit()
    return UserResponse(**user.dict())


@router.get("/{user_id}", response_model=UserResponse, status_code=HTTPStatus.OK)
async def get_user(
    user_id: UUID4,
    session: Session = Depends(db_session),
) -> UserResponse:
    client_repository = UserRepository(session)
    return UserResponse(**client_repository.get_by_id(user_id=user_id).dict())
