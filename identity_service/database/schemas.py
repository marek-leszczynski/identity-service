import re

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import as_declarative, declared_attr
from sqlalchemy.sql import func

class_registry: dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    _table_name_pattern = re.compile(r"(?<!^)(?=[A-Z])")

    created_at = Column(DateTime(timezone=True), server_default=func.now)  # type: ignore[arg-type]
    updated_at = Column(DateTime(timezone=True), onupdate=func.now)

    __name__: str

    @declared_attr.directive
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        return cls._table_name_pattern.sub("_", cls.__name__).lower()
