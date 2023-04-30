from sqlalchemy import Column, Uuid

from ..database import Base


class HealthCheck(Base):
    id = Column(Uuid(), primary_key=True)
