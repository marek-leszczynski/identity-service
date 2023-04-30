import typing as T
from enum import Enum

from psycopg2.errors import (  # pylint: disable=no-name-in-module
    ForeignKeyViolation,
    UniqueViolation,
)
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query, Session

from .exceptions import ObjectAlreadyExists, RelatedObjectNotFound
from .schemas import Base


class SQLAlchemyRepository:
    _model_class: T.Type[Base]

    def __init__(self, session: Session) -> None:
        self._session = session

    def __init_subclass__(cls, *, model_class: T.Type[Base]) -> None:
        cls._model_class = model_class

    def _get_query(self, *criteria) -> Query:  # type: ignore
        return self._session.query(self._model_class).filter(*criteria)

    def _apply_ordering(
        self,
        query: Query,
        order_by: T.List[str],
        record_model: T.Optional[T.Type[Base]] = None,
    ) -> Query:
        for value in order_by:
            if value.startswith("-"):
                query = query.order_by(
                    getattr(record_model or self._model_class, value[1:]).desc()
                )
            else:
                query = query.order_by(
                    getattr(record_model or self._model_class, value).asc()
                )

        return query

    def _apply_filters(self, query: Query, filters: dict) -> Query:
        for key, value in filters.items():
            if isinstance(value, Enum):
                value = value.value
            if isinstance(value, str):
                query = query.filter(
                    func.lower(getattr(self._model_class, key)) == func.lower(value)
                )
            elif isinstance(value, list):
                query = query.filter(getattr(self._model_class, key).in_(value))
            else:
                query = query.filter(getattr(self._model_class, key) == value)
        return query

    def _flush(self) -> None:
        try:
            self._session.flush()
        except IntegrityError as exc:
            if isinstance(exc.orig, ForeignKeyViolation):
                raise RelatedObjectNotFound from exc
            if isinstance(exc.orig, UniqueViolation):
                raise ObjectAlreadyExists from exc
            raise

    def _get_related_schema_class(self, relation_name: str) -> Base:
        return self._model_class.__mapper__.relationships[  # type: ignore
            relation_name
        ].entity.class_
