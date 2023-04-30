from sqlalchemy import ARRAY, Column, Text, Uuid

from identity_service.database import Base


class Client(Base):
    id = Column(Uuid(), primary_key=True)
    secret_hash = Column(Text())
    public_key = Column(Text())
    permissions: Column[list] = Column(ARRAY(Text()))
