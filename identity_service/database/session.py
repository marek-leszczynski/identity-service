import functools
import json
import typing as T

from pydantic.json import pydantic_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from ..settings import settings

json_serializer = functools.partial(json.dumps, default=pydantic_encoder)


engine = create_engine(
    settings.url,
    json_serializer=json_serializer,
    pool_size=settings.database_connection_pool_size,
    max_overflow=settings.database_connection_max_overflow,
    pool_pre_ping=True,
)
session_factory = sessionmaker(bind=engine, autocommit=False)


def db_session() -> T.Generator[Session, None, None]:
    with session_factory() as session:
        yield session
