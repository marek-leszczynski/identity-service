import typing as T

from pydantic import UUID4
from sqlalchemy.exc import NoResultFound

from identity_service.database import ObjectNotFound, SQLAlchemyRepository

from .models import ClientCreate, ClientRead, ClientUpdate
from .schemas import Client


class ClientRepository(SQLAlchemyRepository, model_class=Client):
    _model_class: T.Type[Client]

    def _get_by_id(self, client_id: UUID4) -> Client:
        try:
            return self._get_query(self._model_class.id == client_id).one()
        except NoResultFound as exc:
            raise ObjectNotFound from exc

    def get_by_id(self, client_id: UUID4) -> ClientRead:
        return ClientRead.from_orm(self._get_by_id(client_id=client_id))

    def create(self, *, obj: ClientCreate) -> ClientRead:
        client = self._model_class(**obj.dict())
        self._session.add(client)
        self._flush()

        return ClientRead.from_orm(client)

    def update(self, *, obj: ClientUpdate) -> ClientRead:
        client = self._get_by_id(client_id=obj.id)
        for key, value in obj.dict(exclude_unset=True).items():
            setattr(client, key, value)
        self._flush()

        return ClientRead.from_orm(client)
