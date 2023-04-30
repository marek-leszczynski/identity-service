import typing as T

from sqlalchemy.exc import NoResultFound

from identity_service.database import (
    ObjectAlreadyExists,
    ObjectNotFound,
    SQLAlchemyRepository,
)

from .models import ServiceConfigCreate, ServiceConfigRead, ServiceConfigUpdate
from .schemas import ServiceConfig


class ServiceConfigRepository(SQLAlchemyRepository, model_class=ServiceConfig):
    _model_class: T.Type[ServiceConfig]

    def _get(self) -> ServiceConfig:
        try:
            return self._get_query().one()
        except NoResultFound as exc:
            raise ObjectNotFound from exc

    def get(self) -> ServiceConfigRead:
        return ServiceConfigRead.from_orm(self._get())

    def create(self, *, obj: ServiceConfigCreate) -> ServiceConfigRead:
        try:
            self._get()
        except ObjectNotFound:
            pass
        else:
            raise ObjectAlreadyExists

        service_config = self._model_class(**obj.dict())
        self._session.add(service_config)
        self._flush()

        return ServiceConfigRead.from_orm(service_config)

    def update(self, *, obj: ServiceConfigUpdate) -> ServiceConfigRead:
        service_config = self._get()
        for key, value in obj.dict(exclude_unset=True).items():
            setattr(service_config, key, value)
        self._flush()

        return ServiceConfigRead.from_orm(service_config)
