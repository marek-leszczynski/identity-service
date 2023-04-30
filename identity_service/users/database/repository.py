import typing as T

from pydantic import UUID4
from sqlalchemy.exc import NoResultFound

from identity_service.database import ObjectNotFound, SQLAlchemyRepository

from .models import UserCreate, UserRead, UserUpdate
from .schemas import User


class UserRepository(SQLAlchemyRepository, model_class=User):
    _model_class: T.Type[User]

    def _get_by_id(self, user_id: UUID4) -> User:
        try:
            return self._get_query(self._model_class.id == user_id).one()
        except NoResultFound as exc:
            raise ObjectNotFound from exc

    def _get_by_username(self, username: str) -> User:
        try:
            return self._get_query(self._model_class.username == username).one()
        except NoResultFound as exc:
            raise ObjectNotFound from exc

    def get_by_id(self, user_id: UUID4) -> UserRead:
        return UserRead.from_orm(self._get_by_id(user_id=user_id))

    def get_by_username(self, username: str) -> UserRead:
        return UserRead.from_orm(self._get_by_username(username=username))

    def create(self, *, obj: UserCreate) -> UserRead:
        user = self._model_class(**obj.dict())
        self._session.add(user)
        self._flush()

        return UserRead.from_orm(user)

    def update(self, *, obj: UserUpdate) -> UserRead:
        user = self._get_by_id(user_id=obj.id)
        for key, value in obj.dict(exclude_unset=True).items():
            setattr(user, key, value)
        self._flush()

        return UserRead.from_orm(user)
